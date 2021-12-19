from typing import List

from bs4 import Tag

BLOCK_TAGS = (
    "div",
    "h1",
    "h2",
    "h3",
    "hr",
    "ul",
    "ol",
    "hr",
    "table",
    "en-crypt",
    "en-media",
    "img",
)


def extract_nested_blocks(root: Tag):
    """Extract all block types to the document root
    new Evernote does something similar, while old one allowed to nest them
    """

    for child in root.children:
        # may be strings inside root (hopefully only empty linebreaks)
        # also skip special blocks, like weblicp with images
        if not isinstance(child, Tag) or _is_div_special_block(child):
            continue

        # tables, pictures (or files), encrypted blocks
        subblocks = child.find_all(["img", "en-media", "table", "en-crypt"])

        # special evernote blocks
        subblocks += filter(_is_div_special_block, child.find_all("div"))

        child.insert_after(*subblocks)


def flatten_root(root: Tag):
    """Make sure that each <div> block represents single paragraph
    BAD                     | GOOD
    <en-note>               | <en-note>
     <div>                  |  <div>paragraph1</div>
      <div>paragraph1</div> |  <div>paragraph2</div>
      <div>paragraph2</div> |  <div><br /></div>
     </div>                 | </en-note>
     <div><br /></div>      |
    </en-note>              |
    """

    while True:
        divs_with_blocks = [
            d
            for d in root.find_all("div", recursive=False)
            if _is_element_has_direct_blocks(d) and not _is_div_special_block(d)
        ]

        if not divs_with_blocks:
            break

        for div in divs_with_blocks:
            div.insert_after(*_group_inline_tags(list(div.contents)))

            div.extract()


def _group_inline_tags(elements: List[Tag]):
    blocks = []
    group = []

    for tag in elements:
        is_inline_tag = tag.name not in BLOCK_TAGS

        if is_inline_tag:
            group.append(tag)
        else:
            if group:
                blocks.append(_make_block(group))
                group = []

            blocks.append(tag)

    if group:
        blocks.append(_make_block(group))

    return blocks


def _make_block(elements: List[Tag]):
    """Make a single block from a list of elements"""

    block = Tag(name="div")

    for element in elements:
        block.append(element)

    return block


def _is_element_has_direct_blocks(element):
    return bool(element.find(BLOCK_TAGS, recursive=False))


def _is_div_special_block(element: Tag):
    """Evernote has 3 special blocks that don't have their own tag:
    1. Code blocks
    2. Task
    3. Google drive links
    """

    div_style = element.get("style", "")

    if not div_style:
        return False

    special_block_styles = (
        "en-codeblock",
        "en-task-group",
        "en-richlink",
    )

    return any(block_style in div_style for block_style in special_block_styles)
