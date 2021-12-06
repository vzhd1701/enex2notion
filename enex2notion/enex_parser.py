import base64
import hashlib
import logging
import mimetypes
import re
import uuid
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List
from xml.etree import ElementTree

from dateutil.parser import isoparse

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class EvernoteResource(object):
    data_bin: bytes
    size: int
    md5: str
    mime: str
    file_name: str


@dataclass
class EvernoteNote(object):
    title: str
    created: datetime
    updated: datetime
    content: str  # noqa: WPS110
    tags: List[str]
    author: str
    url: str
    is_webclip: bool
    resources: List[EvernoteResource]
    _note_hash: str = None

    def resource_by_md5(self, md5):
        for resource in self.resources:
            if resource.md5 == md5:
                return resource
        return None

    @property
    def note_hash(self):
        if self._note_hash is None:
            hashable = [
                self.title,
                self.created.isoformat(),
                self.updated.isoformat(),
                self.content,
                "".join(self.tags),
                self.author,
                self.url,
            ]

            s1_hash = hashlib.sha1()
            for h in hashable:
                s1_hash.update(h.encode("utf-8"))
            self._note_hash = s1_hash.hexdigest()  # noqa: WPS601

        return self._note_hash


def iter_notes(enex_file: Path):
    with open(enex_file, "rb") as f:
        context = ElementTree.iterparse(f, events=("start", "end"))

        _, root = next(context)

        for event, elem in context:
            if event == "end" and elem.tag == "note":
                yield _process_note(_etree_to_dict(elem)["note"])

            root.clear()


# https://stackoverflow.com/a/10077069/13100286
def _etree_to_dict(t):  # noqa: WPS210, WPS231, C901
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(_etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {
            t.tag: {
                k: v[0] if len(v) == 1 else v  # noqa: WPS441
                for k, v in dd.items()  # noqa: WPS221
            }
        }
    if t.attrib:
        d[t.tag].update(
            (f"@{k}", v) for k, v in t.attrib.items()  # noqa: WPS221, WPS441
        )
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]["#text"] = text
        else:
            d[t.tag] = text
    return d


def _process_note(note_raw: dict):
    note_attrs = note_raw.get("note-attributes") or {}

    note_tags = note_raw.get("tag", [])
    if isinstance(note_tags, str):
        note_tags = [note_tags]

    note_resources = note_raw.get("resource", [])
    if isinstance(note_resources, dict):
        note_resources = [note_resources]
    resources = [_convert_resource(r) for r in note_resources]

    return EvernoteNote(
        title=note_raw["title"],
        created=isoparse(note_raw["created"]),
        updated=isoparse(note_raw["updated"]),
        content=note_raw["content"],
        tags=note_tags,
        author=note_attrs.get("author", ""),
        url=note_attrs.get("source-url", ""),
        is_webclip=_is_webclip(note_raw),
        resources=resources,
    )


def _is_webclip(note_raw: dict):
    note_attrs = note_raw.get("note-attributes") or {}

    if "web.clip" in note_attrs.get("source", ""):
        return True
    if "webclipper" in note_attrs.get("source-application", ""):
        return True

    return bool(
        re.match('<div[^>]+style="[^"]+en-clipped-content[^"]*"', note_raw["content"])
    )


def _convert_resource(resource_raw):
    res_attr = resource_raw.get("resource-attributes", {})
    if not isinstance(res_attr, dict):
        res_attr = {}

    file_name = res_attr.get("file-name")

    if not file_name:
        ext = mimetypes.guess_extension(resource_raw["mime"]) or ""
        file_name = f"{uuid.uuid4()}{ext}"

    if resource_raw["data"].get("#text"):
        data_bin = base64.b64decode(resource_raw["data"]["#text"])
    else:
        logger.warning("Empty resource")
        data_bin = b""
    data_md5 = hashlib.md5(data_bin).hexdigest()

    return EvernoteResource(
        data_bin=data_bin,
        size=len(data_bin),
        md5=data_md5,
        mime=resource_raw["mime"],
        file_name=file_name,
    )
