import copy
import logging

from bs4 import NavigableString, Tag

from enex2notion.note_parser_blocks import parse_note_blocks

logger = logging.getLogger(__name__)

BLOCK_TAGS = (
    "div",
    "h1",
    "h2",
    "h3",
    "hr",
    "ul",
    "ol",
    "en-media",
    "img",
)

STANDALONE_TAGS = ("en-media", "img", "ol", "ul", "hr")


def parse_webclip(note_dom: Tag):
    """Convert HTML into simplified format, something that Evernote does with "simplify"
    command for webclip notes.

    Keeping in mind all block types from MDN plus a couple of other deprecated ones
    https://developer.mozilla.org/en-US/docs/Web/HTML/Block-level_elements

    Step 1. Delete all elements not fit for display

    Step 2. Unpack all block elements, extracting their content next to them

    Step 3. Convert and prepare before flattening

    We are now left with
    <div> - main paragraph type
    <h1>, <h2>, <h3> - headers
    <hr> - horizontal line
    <ul>, <ol> - lists
    <en-media>, <img> - images
    Plus random mix of various inline elements that will be wrapped in DIV paragraphs

    Lists will be processed separately, so treating them as standalone blocks
    Images and HRs also standalone

    Setp 4. Flatten the tree, so that there are no paragraphs left that contain other
    paragraphs.

    Step 5. Cleanup

    Final. Feed sanitized tree into note parser
    """

    processors = (
        # Preparation
        _remove_unprocessable,
        _unpack_block_elements,
        _unpack_tables,
        # Conversion
        _convert_paragraphs,
        _convert_subheaders,
        _convert_inline_modifiers,
        _convert_textless_links,
        _convert_newlines,
        # Flattening
        _flatten_root,
        # Cleanup
        _remove_empty_blocks,
        _wrap_orphans,
        _strip_paragraphs,
    )

    for processor in processors:
        processor(note_dom)

    return parse_note_blocks(note_dom)


def _remove_unprocessable(root: Tag):
    for e in root.find_all(["nav", "menu", "menuitem"]):
        e.extract()


def _unpack_block_elements(root: Tag):
    container_blocks = [
        "main",
        "section",
        "article",
        "aside",
        "fieldset",
        "form",
        "details",
        "dialog",
        "dd",
        "hgroup",
        "figure",
        "footer",
        "header",
    ]

    for b in container_blocks:
        for e in root.find_all(b):
            e.insert_after(*e.contents)
            e.extract()


def _unpack_tables(root: Tag):
    for cg in root.find_all("colgroup"):
        cg.decompose()

    for b in ("tr", "thead", "tbody", "tfoot", "table"):
        for e in root.find_all(b):
            e.insert_after(*e.contents)
            e.extract()

    _rename_tags(root, ["caption", "td", "th"], "div")


def _convert_paragraphs(root: Tag):
    paragraph_blocks = [
        "address",
        "pre",
        "p",
        "blockquote",
        "dl",
        "dt",
    ]

    _rename_tags(root, paragraph_blocks, "div")


def _convert_subheaders(root: Tag):
    _rename_tags(root, ["h4", "h5", "h6"], "h3")


def _convert_inline_modifiers(root: Tag):
    _rename_tags(root, ["strong"], "b")

    _rename_tags(root, ["em", "cite", "dfn", "abbr", "acronym"], "i")

    _rename_tags(root, ["strike", "del"], "s")


def _convert_textless_links(root: Tag):
    for e in root.find_all("a"):
        if not e.text.strip() and e.get("href"):
            whitespace = (s for s in e.children if isinstance(s, NavigableString))
            for w in whitespace:
                w.extract()

            e.append(e["href"])


def _convert_newlines(root: Tag):
    for e in root.find_all("br"):
        e.replace_with("\n")


def _flatten_root(root: Tag):
    while True:
        elements_with_blocks = [d for d in root.children if _is_element_decomposable(d)]

        if not elements_with_blocks:
            break

        for element in elements_with_blocks:
            if not _is_element_has_direct_blocks(element):
                element.insert_after(*element.children)
                element.extract()
                continue

            _split_by_blocks(element)


def _is_element_decomposable(element):
    if not isinstance(element, Tag):
        return False
    if element.name in STANDALONE_TAGS:
        return False
    return bool(element.find(BLOCK_TAGS))


def _is_element_has_direct_blocks(element):
    return bool(element.find(BLOCK_TAGS, recursive=False))


def _split_by_blocks(element: Tag):
    try:
        block = next(
            c for c in element.children if isinstance(c, Tag) and c.name in BLOCK_TAGS
        )
    except StopIteration:
        return

    next_siblings = list(block.next_siblings)
    element.insert_after(block)

    if next_siblings:
        next_chunk = copy.copy(element)
        next_chunk.clear()

        next_chunk.extend(next_siblings)

        block.insert_after(next_chunk)

        _split_by_blocks(next_chunk)

    if not element.contents:
        element.extract()


def _remove_empty_blocks(root: Tag):
    for element in root.contents.copy():
        if isinstance(element, Tag) and element.name in STANDALONE_TAGS:
            continue

        if not element.text.strip():
            element.extract()


def _wrap_orphans(root: Tag):
    paragraphs = ("div", "h1", "h2", "h3")

    for element in root.contents.copy():
        if isinstance(element, Tag) and element.name in STANDALONE_TAGS + paragraphs:
            continue

        _convert_to_paragraph(element)


def _convert_to_paragraph(element):
    div = Tag(name="div")

    element.insert_after(div)

    div.append(element)


def _strip_paragraphs(root: Tag):
    for e in root.find_all("div"):
        if not e.contents:
            continue

        _strip_left(e)
        _strip_right(e)


def _strip_right(e):
    while isinstance(e.contents[-1], NavigableString):
        rstripped = e.contents[-1].text.rstrip()
        if rstripped:
            e.contents[-1].replace_with(rstripped)
            break
        else:
            e.contents[-1].extract()


def _strip_left(e):
    while isinstance(e.contents[0], NavigableString):
        lstripped = e.contents[0].text.lstrip()
        if lstripped:
            e.contents[0].replace_with(lstripped)
            break
        else:
            e.contents[0].extract()


def _rename_tags(root: Tag, tags_to_rename: list, new_name: str):
    for e in root.find_all(tags_to_rename):
        e.name = new_name
