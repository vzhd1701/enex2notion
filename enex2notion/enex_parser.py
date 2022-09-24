import base64
import hashlib
import logging
import mimetypes
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import Iterator

from dateutil.parser import isoparse

from enex2notion.enex_parser_xml import (
    iter_process_xml_elements,
    iter_xml_elements_as_dict,
)
from enex2notion.enex_types import EvernoteNote, EvernoteResource

logger = logging.getLogger(__name__)


def count_notes(enex_file: Path) -> int:
    return sum(iter_process_xml_elements(enex_file, "note", lambda e: 1))


def iter_notes(enex_file: Path) -> Iterator[EvernoteNote]:
    yield from (_process_note(e) for e in iter_xml_elements_as_dict(enex_file, "note"))


def _process_note(note_raw: dict) -> EvernoteNote:
    if not note_raw:
        note_raw = {}

    note_raw["note-attributes"] = note_raw.get("note-attributes") or {}

    note_tags = note_raw.get("tag", [])
    if isinstance(note_tags, str):
        note_tags = [note_tags]

    now = datetime.now()
    date_created = isoparse(note_raw.get("created", now.isoformat()))
    date_updated = isoparse(note_raw.get("updated", date_created.isoformat()))

    return EvernoteNote(
        title=note_raw.get("title", "Untitled"),
        created=date_created,
        updated=date_updated,
        content=note_raw.get("content", ""),
        tags=note_tags,
        author=note_raw["note-attributes"].get("author", ""),
        url=note_raw["note-attributes"].get("source-url", ""),
        is_webclip=_is_webclip(note_raw),
        resources=_parse_resources(note_raw),
    )


def _parse_resources(note_raw):
    note_resources = note_raw.get("resource", [])

    if isinstance(note_resources, dict):
        note_resources = [note_resources]

    return [_convert_resource(r) for r in note_resources]


def _is_webclip(note_raw: dict):
    note_attrs = note_raw.get("note-attributes") or {}

    if "web.clip" in note_attrs.get("source", ""):
        return True
    if "webclipper" in note_attrs.get("source-application", ""):
        return True

    return bool(
        re.search(
            '<div[^>]+style="[^"]+en-clipped-content[^"]*"', note_raw.get("content", "")
        )
    )


def _convert_resource(resource_raw):
    res_attr = resource_raw.get("resource-attributes", {})
    if not isinstance(res_attr, dict):
        res_attr = {}

    file_name = res_attr.get("file-name")
    file_mime = resource_raw.get("mime", "application/octet-stream")

    if not file_name:
        ext = mimetypes.guess_extension(file_mime) or ".bin"
        file_name = f"{uuid.uuid4()}{ext}"
    elif "." not in file_name:
        ext = mimetypes.guess_extension(file_mime) or ".bin"
        file_name = f"{file_name}{ext}"

    if _is_banned_extension(file_name):
        logger.warning(
            f"'{file_name}' attachment extension is banned,"
            f" will be uploaded as '{file_name}.bin'"
        )

        file_name = f"{file_name}.bin"
        file_mime = "application/octet-stream"

    if resource_raw.get("data", {}).get("#text"):
        data_bin = base64.b64decode(resource_raw["data"]["#text"])
    else:
        logger.debug("Empty resource")
        data_bin = b""
    data_md5 = hashlib.md5(data_bin).hexdigest()

    return EvernoteResource(
        data_bin=data_bin,
        size=len(data_bin),
        md5=data_md5,
        mime=file_mime,
        file_name=file_name,
    )


def _is_banned_extension(filename):
    file_ext = filename.split(".")[-1].lower()
    return file_ext in {
        "apk",
        "app",
        "com",
        "ear",
        "elf",
        "exe",
        "ipa",
        "jar",
        "js",
        "xap",
        "xbe",
        "xex",
        "xpi",
    }
