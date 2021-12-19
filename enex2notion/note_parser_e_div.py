import logging
import re

from bs4 import Tag

from enex2notion.notion_blocks import NotionBookmarkBlock, NotionTextBlock
from enex2notion.notion_blocks_container import NotionCodeBlock
from enex2notion.notion_blocks_list import NotionTodoBlock
from enex2notion.string_extractor import extract_string

logger = logging.getLogger(__name__)


def parse_div(element: Tag):
    style = element.get("style", "")

    # Tasks, skipping those
    if "en-task-group" in style:
        logger.debug("Skipping task block")
        return None

    # Google drive links
    if "en-richlink" in style:
        return parse_richlink(element)

    # Code blocks
    if "en-codeblock" in style:
        return parse_codeblock(element)

    # Text paragraph
    return parse_text(element)


def parse_codeblock(element: Tag):
    return NotionCodeBlock(text_prop=extract_string(element))


def parse_text(element: Tag):
    element_text = extract_string(element)

    todo = element.find("en-todo")
    if todo:
        is_checked = todo.get("checked") == "true"
        return NotionTodoBlock(text_prop=element_text, checked=is_checked)

    return NotionTextBlock(text_prop=element_text)


def parse_richlink(element: Tag):
    url = re.match(".*en-href:(.*?);", element["style"]).group(1).strip()

    return NotionBookmarkBlock(url=url)
