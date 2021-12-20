import hashlib
import logging
import mimetypes
import re

from bs4 import Tag
from w3lib.url import parse_data_uri

from enex2notion.enex_types import EvernoteResource
from enex2notion.notion_blocks_embeddable import NotionImageEmbedBlock
from enex2notion.notion_blocks_uploadable import (
    NotionAudioBlock,
    NotionFileBlock,
    NotionImageBlock,
    NotionPDFBlock,
    NotionVideoBlock,
)
from enex2notion.notion_filetypes import (
    NOTION_AUDIO_MIMES,
    NOTION_IMAGE_MIMES,
    NOTION_VIDEO_MIMES,
)

logger = logging.getLogger(__name__)


def parse_media(element: Tag):
    type_map = {
        NOTION_IMAGE_MIMES: NotionImageBlock,
        NOTION_VIDEO_MIMES: NotionVideoBlock,
        NOTION_AUDIO_MIMES: NotionAudioBlock,
        ("application/pdf",): NotionPDFBlock,
    }

    for types, block_type in type_map.items():
        if element["type"] in types:
            return _parse_media(block_type, element)

    return NotionFileBlock(md5_hash=element["hash"])


def parse_img(element: Tag):
    w, h = _parse_dimensions(element)
    src = element.get("src", "")

    if not src.startswith("data:"):
        return NotionImageEmbedBlock(
            width=w,
            height=h,
            url=src,
        )

    img_resource = _parse_img_resource(src)

    # Make SVG small by default to avoid them spreading too much
    if "svg" in img_resource.mime and not any((w, h)):
        w, h = 50, 50

    return NotionImageBlock(
        width=w,
        height=h,
        md5_hash=img_resource.md5,
        resource=img_resource,
    )


def _parse_img_resource(bin_src: str):
    img_data = parse_data_uri(bin_src)
    img_md5 = hashlib.md5(img_data.data).hexdigest()
    img_ext = mimetypes.guess_extension(img_data.media_type) or ""

    return EvernoteResource(
        data_bin=img_data.data,
        size=len(img_data.data),
        md5=img_md5,
        mime=img_data.media_type,
        file_name=f"{img_md5}{img_ext}",
    )


def _parse_media(block_type, element):
    block = block_type(md5_hash=element["hash"])

    w, h = _parse_dimensions(element)

    # Make SVG small by default to avoid them spreading too much
    if "svg" in element["type"] and not any((w, h)):
        w, h = 50, 50

    block.width = w
    block.height = h

    return block


def _parse_dimensions(element: Tag):
    """Media blocks can have 2 size attributes
    1. --en-naturalWidth, --en-naturalHeight to store original size
    2. width, height to store user set size

    user set - priority
    original - fallback

    <en-media style="--en-naturalWidth:800; --en-naturalHeight:600;" width="150px"
     hash="c491f9f01343c4c79404405f8e35b896" type="image/jpeg" />
    """

    width, height = _parse_dimensions_user_set(element)

    if width or height:
        return width, height

    return _parse_dimensions_original(element)


def _parse_dimensions_user_set(element):
    width_m = re.match("^([0-9]+)", element.get("width", ""))
    width = int(width_m.group(1)) if width_m else None

    height_m = re.match("^([0-9]+)", element.get("height", ""))
    height = int(height_m.group(1)) if height_m else None

    return width, height


def _parse_dimensions_original(element):
    width_m = re.match(".*en-naturalWidth:(.*?);", element.get("style", ""))
    width = int(width_m.group(1)) if width_m else None

    height_m = re.match(".*en-naturalHeight:(.*?);", element.get("style", ""))
    height = int(height_m.group(1)) if height_m else None

    return width, height
