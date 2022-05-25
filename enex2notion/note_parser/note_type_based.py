from typing import List

from bs4 import Tag

from enex2notion.enex_types import EvernoteNote
from enex2notion.note_parser.blocks import parse_note_blocks
from enex2notion.note_parser.webclip import parse_webclip
from enex2notion.note_parser.webclip_pdf import parse_webclip_to_pdf
from enex2notion.notion_blocks.base import NotionBaseBlock


def parse_note_blocks_based_on_type(
    note: EvernoteNote, note_dom: Tag, is_add_pdf_preview: bool, mode_webclips: str
) -> List[NotionBaseBlock]:
    if note.is_webclip:
        if mode_webclips == "PDF":
            return parse_webclip_to_pdf(note, note_dom, is_add_pdf_preview)

        return parse_webclip(note_dom)

    return parse_note_blocks(note_dom)
