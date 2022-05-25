from bs4 import Tag

from enex2notion.note_parser.string_extractor import extract_string
from enex2notion.notion_blocks.header import (
    NotionHeaderBlock,
    NotionSubheaderBlock,
    NotionSubsubheaderBlock,
)


def parse_header(element: Tag):
    header_map = {
        "h1": NotionHeaderBlock,
        "h2": NotionSubheaderBlock,
        "h3": NotionSubsubheaderBlock,
    }
    header_type = header_map[element.name]

    return header_type(text_prop=extract_string(element))
