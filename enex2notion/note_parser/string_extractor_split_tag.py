import copy
from typing import List, Union

from bs4 import NavigableString, PageElement, Tag

STANDALONES = ("h1", "h2", "h3", "div")


def split_tag(tag: Tag) -> List[Tag]:
    """
    Element is either a single div itself or a collection of div or h1-3 "lines"
    it can also contain random inline strings, so we group them in separate lines
    """

    if tag.find_all(STANDALONES):
        return _split_line(copy.copy(tag))

    return [tag]


def _split_line(element: Tag) -> List[Tag]:
    blocks = []
    group = []

    for sub in element.children:
        if _is_inline(sub):
            # skip mid-tag whitespaces
            if not _is_whitespace(sub):
                group.append(sub)

        else:
            if group:
                blocks.append(_make_block(group))
                group = []

            blocks.append(sub)

    if group:
        blocks.append(_make_block(group))

    return blocks


def _is_whitespace(element: PageElement) -> bool:
    return isinstance(element, NavigableString) and not element.text.strip()


def _is_inline(element: Union[Tag, PageElement]) -> bool:
    return not isinstance(element, Tag) or element.name not in STANDALONES


def _make_block(elements: List[Union[Tag, PageElement]]) -> Tag:
    """Make a single block from a list of elements"""

    block = Tag(name="div")

    for element in elements:
        block.append(copy.copy(element))

    return block
