import logging
from typing import Optional

from bs4 import BeautifulSoup, Tag

from enex2notion.enex_types import EvernoteNote
from enex2notion.note_parser.note_post_process_condense import condense_lines
from enex2notion.note_parser.note_post_process_resources import resolve_resources
from enex2notion.note_parser.note_type_based import parse_note_blocks_based_on_type
from enex2notion.notion_blocks.container import NotionCalloutBlock
from enex2notion.notion_blocks.text import TextProp
from enex2notion.utils_static import Rules

logger = logging.getLogger(__name__)


def parse_note(note: EvernoteNote, rules: Rules):
    note_dom = _parse_note_dom(note)
    if note_dom is None:
        return []

    note_blocks = parse_note_blocks_based_on_type(
        note, note_dom, rules.add_pdf_preview, rules.mode_webclips
    )

    if rules.condense_lines_sparse:
        note_blocks = condense_lines(note_blocks, is_sparse=True)
    elif rules.condense_lines:
        note_blocks = condense_lines(note_blocks)

    if rules.add_meta:
        _add_meta(note_blocks, note)

    resolve_resources(note_blocks, note)

    return note_blocks


def _parse_note_dom(note: EvernoteNote) -> Optional[Tag]:
    # Using html.parser because Evernote enml2 is basically HTML
    note_dom = BeautifulSoup(note.content, "html.parser").find("en-note")

    if not isinstance(note_dom, Tag):
        logger.error(f"Failed to extract DOM from note '{note.title}'")
        return None

    return _filter_yinxiang_markdown(note_dom)


def _filter_yinxiang_markdown(note_dom: Tag) -> Tag:
    last_block = note_dom.contents[-1]

    if last_block and "display:none" in last_block.attrs.get("style", ""):
        last_block.extract()

    return note_dom


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
