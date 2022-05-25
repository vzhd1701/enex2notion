from typing import List

from enex2notion.notion_blocks.base import NotionBaseBlock
from enex2notion.notion_blocks.text import NotionTextBlock, TextProp


class LineCondenser(object):
    def __init__(self, is_sparse: bool):
        self.result_blocks = []
        self.solid_block = None

        self.is_sparse = is_sparse

    @property
    def final_blocks(self):
        self._start_new_solid_block()

        return self.result_blocks

    def add_block(self, b):
        if _is_empty_paragraph(b) or not isinstance(b, NotionTextBlock):
            self._start_new_solid_block()

            if not _is_empty_paragraph(b) or self.is_sparse:
                self.result_blocks.append(b)

        else:
            self._add_to_solid_block(b)

            if b.children:
                self.solid_block.children = b.children
                self._start_new_solid_block()

    def _start_new_solid_block(self):
        if self.solid_block:
            self.result_blocks.append(self.solid_block)
            self.solid_block = None

    def _add_to_solid_block(self, b):
        if self.solid_block:
            self.solid_block = NotionTextBlock(
                text_prop=_concat_text_props(self.solid_block.text_prop, b.text_prop)
            )
        else:
            self.solid_block = b


def condense_lines(blocks: List[NotionBaseBlock], is_sparse=False):
    condenser = LineCondenser(is_sparse)

    blocks = _join_empty_paragraphs(blocks)

    for b in blocks:
        b.children = condense_lines(b.children)
        condenser.add_block(b)

    return _strip_paragraphs(condenser.final_blocks)


def _strip_paragraphs(blocks: List[NotionBaseBlock]):
    result_blocks = []

    for b in blocks:
        if isinstance(b, NotionTextBlock):
            b.text_prop = b.text_prop.strip()

        result_blocks.append(b)

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
        return block.text_prop.text.strip() == ""
    return False


def _concat_text_props(text_prop1: TextProp, text_prop2: TextProp) -> TextProp:
    return TextProp(
        text=f"{text_prop1.text}\n{text_prop2.text}",
        properties=text_prop1.properties + [["\n"]] + text_prop2.properties,
    )
