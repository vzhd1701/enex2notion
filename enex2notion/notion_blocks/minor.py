from notion import block

from enex2notion.notion_blocks.base import NotionBaseBlock


class NotionDividerBlock(NotionBaseBlock):
    type = block.DividerBlock


class NotionBookmarkBlock(NotionBaseBlock):
    type = block.BookmarkBlock

    def __init__(self, url, **kwargs):
        super().__init__(**kwargs)

        self.attrs["link"] = url
