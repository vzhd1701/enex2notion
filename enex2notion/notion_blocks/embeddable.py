from notion import block

from enex2notion.notion_blocks.base import NotionBaseBlock


class NotionEmbedBlock(NotionBaseBlock):
    def __init__(self, width=None, height=None, url=None, **kwargs):
        super().__init__(**kwargs)

        self.width = width
        self.height = height
        self.source_url = url

    @property
    def height(self):
        return self.attrs.get("height")

    @height.setter
    def height(self, height):
        if height is not None:
            self.attrs["height"] = height

    @property
    def width(self):
        return self.attrs.get("width")

    @width.setter
    def width(self, width):
        if width is not None:
            self.attrs["width"] = width

    @property
    def source_url(self):
        return self.attrs.get("display_source")

    @source_url.setter
    def source_url(self, source_url):
        if source_url is not None:
            self.attrs["display_source"] = source_url
            self.attrs["source"] = source_url


class NotionImageEmbedBlock(NotionEmbedBlock):
    type = block.ImageBlock
