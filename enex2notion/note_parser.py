from bs4 import BeautifulSoup

from enex2notion.enex_types import EvernoteNote
from enex2notion.note_parser_dom import logger, parse_note_dom
from enex2notion.notion_blocks import TextProp
from enex2notion.notion_blocks_container import NotionCalloutBlock
from enex2notion.notion_blocks_uploadable import NotionUploadableBlock


def parse_note(note: EvernoteNote, is_meta_attached: bool):
    logger.debug(f"Parsing note '{note.title}'...")

    note_dom = BeautifulSoup(note.content, "html.parser").find("en-note")

    if not note_dom:
        logger.error(f"Failed to extract DOM from note '{note.title}'")
        return []

    note_blocks = parse_note_dom(note_dom)

    _resolve_resources(note_blocks, note)

    # Add metadata block
    if is_meta_attached:
        note_blocks.insert(
            0,
            NotionCalloutBlock(
                icon="ℹ️",
                text_prop=TextProp(_get_note_meta(note)),
            ),
        )

    return note_blocks


def _resolve_resources(note_blocks, note: EvernoteNote):
    for block in note_blocks.copy():
        # Resolve resource hash to actual resource
        if isinstance(block, NotionUploadableBlock) and block.resource is None:
            block.resource = note.resource_by_md5(block.md5_hash)

            if block.resource is None:
                logger.warning(f"Failed to resolve resource in '{note.title}'")
                note_blocks.remove(block)


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
