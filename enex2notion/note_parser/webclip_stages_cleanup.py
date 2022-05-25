from bs4 import NavigableString, Tag

from enex2notion.note_parser.webclip_stages_common import STANDALONE_TAGS


def remove_empty_blocks(root: Tag):
    for element in root.contents.copy():
        if isinstance(element, Tag) and element.name in STANDALONE_TAGS:
            continue

        if not element.text.strip():
            element.extract()


def wrap_orphans(root: Tag):
    paragraphs = ("div", "h1", "h2", "h3")

    for element in root.contents.copy():
        if isinstance(element, Tag) and element.name in STANDALONE_TAGS + paragraphs:
            continue

        _convert_to_paragraph(element)


def _convert_to_paragraph(element):
    div = Tag(name="div")

    element.insert_after(div)

    div.append(element)


def strip_paragraphs(root: Tag):
    for e in root.find_all("div"):
        if not e.contents:
            continue

        _strip_left(e)
        _strip_right(e)


def _strip_right(e):
    while e.contents and isinstance(e.contents[-1], NavigableString):
        rstripped = e.contents[-1].text.rstrip()
        if rstripped:
            e.contents[-1].replace_with(rstripped)
            break
        else:
            e.contents[-1].extract()


def _strip_left(e):
    while e.contents and isinstance(e.contents[0], NavigableString):
        lstripped = e.contents[0].text.lstrip()
        if lstripped:
            e.contents[0].replace_with(lstripped)
            break
        else:
            e.contents[0].extract()
