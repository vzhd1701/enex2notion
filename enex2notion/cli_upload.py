import itertools
import logging
from pathlib import Path
from typing import Optional

from enex2notion.enex_parser import count_notes, iter_notes
from enex2notion.enex_types import EvernoteNote
from enex2notion.enex_uploader import upload_note
from enex2notion.enex_uploader_modes import get_notebook_database, get_notebook_page
from enex2notion.note_parser.note import parse_note
from enex2notion.utils_exceptions import NoteUploadFailException
from enex2notion.utils_static import Rules

logger = logging.getLogger(__name__)


class DoneFile(object):
    def __init__(self, path: Path):
        self.path = path

        try:
            with open(path, "r") as f:
                self.done_hashes = {line.strip() for line in f}
        except FileNotFoundError:
            self.done_hashes = set()

    def __contains__(self, note_hash):
        return note_hash in self.done_hashes

    def add(self, note_hash):
        self.done_hashes.add(note_hash)

        with open(self.path, "a") as f:
            f.write(f"{note_hash}\n")


class EnexUploader(object):
    def __init__(self, import_root, mode: str, done_file: Optional[Path], rules: Rules):
        self.import_root = import_root
        self.mode = mode

        self.rules = rules

        self.done_hashes = DoneFile(done_file) if done_file else set()

        self.notebook_root = None
        self.notebook_notes_count = None

    def upload_notebook(self, enex_file: Path):
        logger.info(f"Processing notebook '{enex_file.stem}'...")

        try:
            self.notebook_root = self._get_notebook_root(enex_file.stem)
        except NoteUploadFailException:
            if not self.rules.skip_failed:
                raise
            return

        self.notebook_notes_count = count_notes(enex_file)

        logger.debug(
            f"'{enex_file.stem}' notebook contains {self.notebook_notes_count} note(s)"
        )

        for note_idx, note in enumerate(iter_notes(enex_file), 1):
            self.upload_note(note, note_idx)

    def upload_note(self, note: EvernoteNote, note_idx: int):
        if note.note_hash in self.done_hashes:
            logger.debug(f"Skipping note '{note.title}' (already uploaded)")
            return

        if self.rules.tag and self.rules.tag not in note.tags:
            note.tags.append(self.rules.tag)

        logger.debug(f"Parsing note '{note.title}'")

        note_blocks = self._parse_note(note)
        if not note_blocks:
            logger.debug(f"Skipping note '{note.title}' (no blocks)")
            return

        if self.notebook_root is not None:
            logger.info(
                f"Uploading note {note_idx}"
                f" out of {self.notebook_notes_count} '{note.title}'"
            )

            try:
                self._upload_note(self.notebook_root, note, note_blocks)
            except NoteUploadFailException:
                if not self.rules.skip_failed:
                    raise
                return

            self.done_hashes.add(note.note_hash)

    def _parse_note(self, note):
        try:
            return parse_note(note, self.rules)
        except Exception as e:
            logger.error(f"Failed to parse note '{note.title}'")
            logger.debug(e, exc_info=e)
            return []

    def _get_notebook_root(self, notebook_title):
        if self.import_root is None:
            return None

        error_message = f"Failed to get notebook root for '{notebook_title}'"
        get_func = get_notebook_database if self.mode == "DB" else get_notebook_page

        return self._attempt_upload(
            get_func, error_message, self.import_root, notebook_title
        )

    def _upload_note(self, notebook_root, note, note_blocks):
        self._attempt_upload(
            upload_note,
            f"Failed to upload note '{note.title}' to Notion",
            notebook_root,
            note,
            note_blocks,
            self.rules.keep_failed,
        )

    def _attempt_upload(self, upload_func, error_message, *args, **kwargs):
        for attempt in itertools.count(1):
            try:
                return upload_func(*args, **kwargs)
            except NoteUploadFailException as e:
                logger.debug(f"Upload error: {e}", exc_info=e)

                if attempt == self.rules.retry:
                    logger.error(f"{error_message}!")
                    raise

                logger.warning(f"{error_message}! Retrying...")
