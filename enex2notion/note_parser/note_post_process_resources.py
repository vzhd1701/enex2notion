import logging

from enex2notion.enex_types import EvernoteNote
from enex2notion.notion_blocks.uploadable import NotionUploadableBlock

logger = logging.getLogger(__name__)


def resolve_resources(note_blocks, note: EvernoteNote):
    for block in note_blocks.copy():
        # Resolve resource hash to actual resource
        if isinstance(block, NotionUploadableBlock) and block.resource is None:
            block.resource = note.resource_by_md5(block.md5_hash)

            if block.resource is None:
                logger.debug(f"Failed to resolve resource in '{note.title}'")
                note_blocks.remove(block)
        if block.children:
            resolve_resources(block.children, note)
