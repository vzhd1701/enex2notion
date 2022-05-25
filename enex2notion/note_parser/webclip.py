import logging

from bs4 import Tag

from enex2notion.note_parser.blocks import parse_note_blocks
from enex2notion.note_parser.webclip_stages_cleanup import (
    remove_empty_blocks,
    strip_paragraphs,
    wrap_orphans,
)
from enex2notion.note_parser.webclip_stages_convert import (
    convert_inline_modifiers,
    convert_newlines,
    convert_paragraphs,
    convert_subheaders,
    convert_textless_links,
)
from enex2notion.note_parser.webclip_stages_flatten import flatten_root
from enex2notion.note_parser.webclip_stages_preparation import (
    remove_unprocessable,
    unpack_block_elements,
    unpack_tables,
)

logger = logging.getLogger(__name__)


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
        remove_unprocessable,
        unpack_block_elements,
        unpack_tables,
        # Conversion
        convert_paragraphs,
        convert_subheaders,
        convert_inline_modifiers,
        convert_textless_links,
        convert_newlines,
        # Flattening
        flatten_root,
        # Cleanup
        remove_empty_blocks,
        wrap_orphans,
        strip_paragraphs,
    )

    for processor in processors:
        processor(note_dom)

    return parse_note_blocks(note_dom)
