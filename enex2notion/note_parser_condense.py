from typing import List

from enex2notion.notion_blocks import NotionBaseBlock
from enex2notion.notion_blocks_text import NotionTextBlock, TextProp


def condense_lines(blocks: List[NotionBaseBlock], is_sparse=False):
    result_blocks = []
    solid_block = None

    blocks = _join_empty_paragraphs(blocks)

    for b in blocks:
        b.children = condense_lines(b.children)

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

    return _strip_paragraphs(result_blocks)


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
        text=text_prop1.text + "\n" + text_prop2.text,
        properties=text_prop1.properties + [["\n"]] + text_prop2.properties,
    )
