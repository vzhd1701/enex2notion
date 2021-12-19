import logging

from bs4 import NavigableString, Tag

from enex2notion.note_parser_e_div import parse_div, parse_text
from enex2notion.note_parser_e_media import parse_img, parse_media
from enex2notion.note_parser_e_table import parse_table
from enex2notion.note_parser_elements import parse_encrypt, parse_header, parse_list
from enex2notion.note_parser_helpers import extract_nested_blocks, flatten_root
from enex2notion.note_parser_indented import (
    group_blocks_by_indent,
    is_indentation_inconsistent,
    parse_indented,
    parse_indented_plain,
)
from enex2notion.notion_blocks import NotionDividerBlock, NotionTextBlock, TextProp

logger = logging.getLogger(__name__)


def parse_note_blocks(note: Tag):
    flatten_root(note)

    extract_nested_blocks(note)

    note_blocks = group_blocks_by_indent(note)

    blocks = []

    for child in note_blocks:
        if isinstance(child, list):
            branch = _parse_indented_group(child)

            _append_branch(blocks, branch)

            continue

        block = _parse_block(child)

        if isinstance(block, list):
            blocks.extend(block)
        elif block is not None:
            blocks.append(block)

    return blocks


def _append_branch(blocks, branch):
    if not blocks:
        # add empty textblock as parent, because indent cannot start from root
        blocks.append(NotionTextBlock(text_prop=TextProp(text="")))
    blocks[-1].children.extend(branch)


def _parse_indented_group(child):
    if is_indentation_inconsistent(child):
        logger.debug("Inconsistent indentation detected, parsing as plain")
        return parse_indented_plain(child)

    return parse_indented(child)


def _parse_block(element: Tag):
    tag_map = {
        ("h1", "h2", "h3"): parse_header,
        ("hr",): lambda e: NotionDividerBlock(),
        ("ol", "ul"): parse_list,
        ("table",): parse_table,
        ("en-media",): parse_media,
        ("img",): parse_img,
        ("div",): parse_div,
        ("en-crypt",): parse_encrypt,
    }

    for tags, tag_parser in tag_map.items():
        if element.name in tags:
            return tag_parser(element)

    if isinstance(element, NavigableString):
        if element.text.strip():
            logger.debug("Non-empty string element in root")
            return NotionTextBlock(text_prop=TextProp(text=element.text.strip()))
        return None

    logger.debug(f"Unknown block: {element.name}, parsing as text")
    return parse_text(element)
