import logging

from bs4 import NavigableString, Tag

from enex2notion.notion_blocks import NotionTextBlock, TextProp
from enex2notion.notion_blocks_header import (
    NotionHeaderBlock,
    NotionSubheaderBlock,
    NotionSubsubheaderBlock,
)
from enex2notion.notion_blocks_list import (
    NotionBulletedListBlock,
    NotionNumberedListBlock,
    NotionTodoBlock,
)
from enex2notion.string_extractor import extract_string

logger = logging.getLogger(__name__)


def parse_encrypt(element: Tag):
    logger.warning("Skipping encrypted block")


def parse_list(element: Tag):
    nodes = []

    is_ul = element.name == "ul"

    for subelement in element.children:
        if subelement.name == "li":
            li_item = _parse_list_item(subelement, is_ul)

            nodes.append(li_item)

        elif subelement.name in {"ul", "ol"}:
            if not nodes:
                nodes.append(_make_blank_node(is_ul))

            nodes[-1].children.extend(parse_list(subelement))

        else:
            li_odd_item = _parse_odd_item(subelement)
            if li_odd_item is None:
                continue

            nodes.append(li_odd_item)

    return nodes


def _make_blank_node(is_ul):
    if is_ul:
        return NotionBulletedListBlock(text_prop=TextProp(text=""))

    return NotionNumberedListBlock(text_prop=TextProp(text=""))


def _parse_odd_item(element: Tag):
    if isinstance(element, NavigableString):
        if not element.text.strip():
            return None

        logger.debug("Non-empty string element inside list")
        return NotionTextBlock(text_prop=TextProp(text=element.text.strip()))

    logger.debug(f"Unexpected tag inside list: {element.name}, parsing as text")
    return NotionTextBlock(text_prop=extract_string(element))


def _parse_list_item(list_item, is_ul):
    li_text = extract_string(list_item)

    if is_ul:
        todo = list_item.find("en-todo")
        if todo:
            is_checked = todo.get("checked") == "true"
            return NotionTodoBlock(text_prop=li_text, checked=is_checked)

        return NotionBulletedListBlock(text_prop=li_text)

    return NotionNumberedListBlock(text_prop=li_text)


def parse_header(element: Tag):
    header_map = {
        "h1": NotionHeaderBlock,
        "h2": NotionSubheaderBlock,
        "h3": NotionSubsubheaderBlock,
    }
    header_type = header_map[element.name]

    return header_type(text_prop=extract_string(element))
