import re
from typing import List

from bs4 import Tag

from enex2notion.note_parser_e_div import parse_text

EVERNOTE_INDENT_MARGIN = 40


def group_blocks_by_indent(root: Tag):
    blocks = []
    group = []

    for child in root.children:
        c_indent_level = parse_indent_level(child) if child.name == "div" else 0

        if c_indent_level > 0:
            group.append(child)
        else:
            if group:
                blocks.append(group)
                group = []

            blocks.append(child)

    if group:
        blocks.append(group)

    return blocks


def is_indentation_inconsistent(paragraphs: List[Tag]):
    """Evernote has strict indentation margin of 40px"""

    indent_level = 0

    for cur_paragraph in paragraphs:
        cur_level = parse_indent_level(cur_paragraph)

        if cur_level > indent_level:
            difference = cur_level - indent_level

            if difference != EVERNOTE_INDENT_MARGIN:
                return True

        indent_level = cur_level

    return False


def parse_indent_level(element: Tag):
    indent_match = re.match(
        r".*(padding|margin)-left:\s*([0-9]+)px;", element.get("style", "")
    )

    if not indent_match:
        return 0

    return int(indent_match.group(2))


# https://stackoverflow.com/a/24966533/13100286
def parse_indented(  # noqa: WPS210, WPS231, C901
    paragraphs: List[Tag], indent_level: int = None
):
    """Builds paragraphs tree using indentation levels"""

    result_node = []

    if indent_level is None:
        indent_level = parse_indent_level(paragraphs[0])

    for i, cur_paragraph in enumerate(paragraphs):
        cur_level = parse_indent_level(cur_paragraph)

        try:
            next_level = parse_indent_level(paragraphs[i + 1])
        except IndexError:
            next_level = -1

        # Edge cases
        if cur_level > indent_level:
            continue
        if cur_level < indent_level:
            return result_node

        # Recursion
        if next_level == indent_level:
            result_node.append(parse_text(cur_paragraph))
        elif next_level > indent_level:
            result_node.append(parse_text(cur_paragraph))
            result_node[-1].children = parse_indented(
                paragraphs[i + 1 :], indent_level=next_level
            )
        else:
            result_node.append(parse_text(cur_paragraph))
            return result_node

    return result_node


def parse_indented_plain(paragraphs: List[Tag]):
    result_lines = []

    for cur_paragraph in paragraphs:
        cur_level = parse_indent_level(cur_paragraph) // EVERNOTE_INDENT_MARGIN

        cur_paragraph.insert(0, "    " * cur_level)

        result_lines.append(parse_text(cur_paragraph))

    return result_lines
