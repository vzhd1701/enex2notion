import logging
from typing import List

from bs4 import NavigableString, PageElement, Tag

from enex2notion.note_parser.elements.media import parse_img, parse_media
from enex2notion.note_parser.string_extractor import extract_string
from enex2notion.notion_blocks.base import NotionBaseBlock
from enex2notion.notion_blocks.list import (
    NotionBulletedListBlock,
    NotionNumberedListBlock,
    NotionTodoBlock,
)
from enex2notion.notion_blocks.text import NotionTextBlock, TextProp

logger = logging.getLogger(__name__)


class ListNodes(object):
    def __init__(self, is_ul: bool):
        self.nodes: List[NotionBaseBlock] = []
        self.is_ul = is_ul

    def add_li(self, subelement: Tag) -> None:
        embedded_media = _extract_media(subelement)

        li_item = _parse_list_item(subelement, self.is_ul)

        if embedded_media:
            li_item.children = embedded_media

        self.nodes.append(li_item)

    def add_ul_ol(self, subelement: Tag) -> None:
        if not self.nodes:
            self.nodes.append(_make_blank_node(self.is_ul))

        self.nodes[-1].children.extend(parse_list(subelement))

    def add_odd_one(self, subelement):
        li_odd_item = _parse_odd_item(subelement)

        if li_odd_item is None:
            return

        self.nodes.append(li_odd_item)


def parse_list(element: Tag) -> List[NotionBaseBlock]:
    is_ul = element.name == "ul"

    list_nodes = ListNodes(is_ul)

    for subelement in element.children:
        name = subelement.name if isinstance(subelement, Tag) else None

        if name == "li":
            list_nodes.add_li(subelement)

        elif name in {"ul", "ol"}:
            list_nodes.add_ul_ol(subelement)

        else:
            list_nodes.add_odd_one(subelement)

    return list_nodes.nodes


def _extract_media(element: Tag):
    media = []
    for img in element.find_all(["en-media", "img"]):
        if img.name == "en-media":
            media.append(parse_media(img.extract()))
        else:
            media.append(parse_img(img.extract()))
    return media


def _make_blank_node(is_ul):
    if is_ul:
        return NotionBulletedListBlock(text_prop=TextProp(text=""))

    return NotionNumberedListBlock(text_prop=TextProp(text=""))


def _parse_odd_item(element: PageElement):
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
