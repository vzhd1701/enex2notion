import copy

from bs4 import Tag

from enex2notion.note_parser.webclip_stages_common import BLOCK_TAGS, STANDALONE_TAGS


def flatten_root(root: Tag):
    while True:
        elements_with_blocks = [d for d in root.children if _is_element_decomposable(d)]

        if not elements_with_blocks:
            break

        for element in elements_with_blocks:
            _flatten_element(element)


def _flatten_element(element):
    if not _is_element_has_direct_blocks(element):
        element.insert_after(*element.children)
        element.extract()
        return

    _split_by_blocks(element)


def _is_element_decomposable(element) -> bool:
    if not isinstance(element, Tag):
        return False
    if element.name in STANDALONE_TAGS:
        return False
    return bool(element.find(BLOCK_TAGS))


def _is_element_has_direct_blocks(element):
    return bool(element.find(BLOCK_TAGS, recursive=False))


def _split_by_blocks(element: Tag):
    next_element = element

    while next_element is not None:
        cur_element = next_element

        try:
            block = next(
                c
                for c in cur_element.children
                if isinstance(c, Tag) and c.name in BLOCK_TAGS
            )
        except StopIteration:
            return

        next_siblings = list(block.next_siblings)
        cur_element.insert_after(block)

        if next_siblings:
            # Create an empty clone of the current element
            next_chunk = copy.copy(cur_element)
            next_chunk.clear()

            next_chunk.extend(next_siblings)

            block.insert_after(next_chunk)

            next_element = next_chunk
        else:
            next_element = None

        if not cur_element.contents:
            cur_element.extract()
