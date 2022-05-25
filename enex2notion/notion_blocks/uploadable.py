from notion import block

from enex2notion.notion_blocks.embeddable import NotionEmbedBlock


class NotionUploadableBlock(NotionEmbedBlock):
    def __init__(self, md5_hash, resource=None, **kwargs):
        super().__init__(**kwargs)

        self.md5_hash = md5_hash

        self.resource = resource

    def __eq__(self, other):
        return (
            super().__eq__(other)
            and self.md5_hash == other.md5_hash
            and self.resource == other.resource
        )


class NotionFileBlock(NotionUploadableBlock):
    type = block.FileBlock


class NotionVideoBlock(NotionUploadableBlock):
    type = block.VideoBlock


class NotionAudioBlock(NotionUploadableBlock):
    type = block.AudioBlock


class NotionPDFBlock(NotionUploadableBlock):
    type = block.PDFBlock


class NotionImageBlock(NotionUploadableBlock):
    type = block.ImageBlock
