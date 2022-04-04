import logging

from bs4 import BeautifulSoup

from enex2notion.enex_types import EvernoteNote
from enex2notion.note_parser_blocks import parse_note_blocks
from enex2notion.note_parser_webclip import parse_webclip
from enex2notion.note_parser_webclip_pdf import parse_webclip_to_pdf
from enex2notion.notion_blocks import TextProp
from enex2notion.notion_blocks_container import NotionCalloutBlock
from enex2notion.notion_blocks_uploadable import NotionUploadableBlock

logger = logging.getLogger(__name__)


def parse_note(
    note: EvernoteNote, mode_webclips="TXT", is_add_meta=False, is_add_pdf_preview=False
):
    note_dom = _parse_note_dom(note)
    if not note_dom:
        return []

    if note.is_webclip:
        if mode_webclips == "PDF":
            note_blocks = parse_webclip_to_pdf(note, note_dom, is_add_pdf_preview)
        else:
            note_blocks = parse_webclip(note_dom)
    else:
        note_blocks = parse_note_blocks(note_dom)

    if is_add_meta:
        _add_meta(note_blocks, note)

    _resolve_resources(note_blocks, note)

    _remove_banned_files(note_blocks, note)

    return note_blocks


def _parse_note_dom(note: EvernoteNote):
    note_dom = BeautifulSoup(note.content, "html.parser").find("en-note")

    if not note_dom:
        logger.error(f"Failed to extract DOM from note '{note.title}'")
        return None

    return note_dom


def _resolve_resources(note_blocks, note: EvernoteNote):
    for block in note_blocks.copy():
        # Resolve resource hash to actual resource
        if isinstance(block, NotionUploadableBlock) and block.resource is None:
            block.resource = note.resource_by_md5(block.md5_hash)

            if block.resource is None:
                logger.debug(f"Failed to resolve resource in '{note.title}'")
                note_blocks.remove(block)
        if block.children:
            _resolve_resources(block.children, note)


def _remove_banned_files(note_blocks, note: EvernoteNote):
    for block in note_blocks.copy():
        if isinstance(block, NotionUploadableBlock):
            if _is_banned_extension(block.resource.file_name):
                logger.warning(
                    f"Cannot upload '{block.resource.file_name}' from '{note.title}',"
                    f" this file extensions is banned by Notion"
                )
                note_blocks.remove(block)
        if block.children:
            _remove_banned_files(block.children, note)


def _is_banned_extension(filename):
    file_ext = filename.split(".")[-1]
    return file_ext in {"exe", "com", "js"}


def _add_meta(note_blocks, note: EvernoteNote):
    note_blocks.insert(
        0,
        NotionCalloutBlock(
            icon="ℹ️",
            text_prop=TextProp(_get_note_meta(note)),
        ),
    )


def _get_note_meta(note: EvernoteNote):
    note_meta = [
        "Created: {0}".format(note.created.isoformat()),
        "Updated: {0}".format(note.updated.isoformat()),
    ]

    if note.url:
        note_meta.append(f"URL: {note.url}")

    if note.tags:
        note_tags = ", ".join(note.tags)
        note_meta.append(f"Tags: {note_tags}")

    return "\n".join(note_meta)
