import logging
from typing import List

from bs4 import BeautifulSoup

from enex2notion.enex_types import EvernoteNote
from enex2notion.note_parser_blocks import parse_note_blocks
from enex2notion.note_parser_webclip import parse_webclip
from enex2notion.note_parser_webclip_pdf import parse_webclip_to_pdf
from enex2notion.notion_blocks import NotionBaseBlock, NotionTextBlock, TextProp
from enex2notion.notion_blocks_container import NotionCalloutBlock
from enex2notion.notion_blocks_uploadable import NotionUploadableBlock

logger = logging.getLogger(__name__)


def parse_note(
    note: EvernoteNote,
    mode_webclips="TXT",
    is_add_meta=False,
    is_add_pdf_preview=False,
    is_condense_lines=False,
    is_condense_lines_sparse=False,
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

    if is_condense_lines_sparse:
        note_blocks = _condense_lines(note_blocks, is_sparse=True)
    elif is_condense_lines:
        note_blocks = _condense_lines(note_blocks)

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


def _condense_lines(blocks: List[NotionBaseBlock], is_sparse=False):
    result_blocks = []
    solid_block = None

    blocks = _join_empty_paragraphs(blocks)

    for b in blocks:
        b.children = _condense_lines(b.children)

        if _is_empty_paragraph(b) or not isinstance(b, NotionTextBlock):
            if solid_block:
                result_blocks.append(solid_block)
                solid_block = None

            if not _is_empty_paragraph(b) or is_sparse:
                result_blocks.append(b)

        else:
            if solid_block:
                solid_block = NotionTextBlock(
                    text_prop=_concat_text_props(solid_block.text_prop, b.text_prop)
                )
            else:
                solid_block = b

            if b.children:
                solid_block.children = b.children
                result_blocks.append(solid_block)
                solid_block = None

    if solid_block:
        result_blocks.append(solid_block)

    return result_blocks


def _join_empty_paragraphs(blocks: List[NotionBaseBlock]):
    result_blocks = []
    gap_started = False

    for b in blocks:
        if _is_empty_paragraph(b):
            gap_started = True

        else:
            if gap_started:
                result_blocks.append(NotionTextBlock())
                gap_started = False

            result_blocks.append(b)

    return result_blocks


def _is_empty_paragraph(block: NotionBaseBlock):
    if isinstance(block, NotionTextBlock):
        return block == NotionTextBlock()
    return False


def _concat_text_props(text_prop1: TextProp, text_prop2: TextProp) -> TextProp:
    return TextProp(
        text=text_prop1.text + "\n" + text_prop2.text,
        properties=text_prop1.properties + [["\n"]] + text_prop2.properties,
    )
