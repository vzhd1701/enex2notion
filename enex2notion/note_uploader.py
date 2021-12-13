import requests
from notion.block import FileBlock
from notion.settings import S3_URL_PREFIX

from enex2notion.enex_types import EvernoteResource
from enex2notion.notion_blocks_uploadable import NotionUploadableBlock


def upload_block(root, block):
    new_block = root.children.add_new(block.type, **block.attrs)

    for p_key, p_value in block.properties.items():
        new_block.set(p_key, p_value)

    if isinstance(block, NotionUploadableBlock):
        _upload_file(new_block, block.resource)

    for sub_block in block.children:
        upload_block(new_block, sub_block)


def _upload_file(new_block, resource: EvernoteResource):
    """Copy/paste from EmbedOrUploadBlock class

    changes:
        binary resource.data_bin in put requests instead of file path
        set size and title for FileBlock
    """

    upload_data = new_block._client.post(  # noqa: WPS437
        "getUploadFileUrl",
        {"bucket": "secure", "name": resource.file_name, "contentType": resource.mime},
    ).json()

    response = requests.put(
        upload_data["signedPutUrl"],
        data=resource.data_bin,
        headers={"Content-type": resource.mime},
    )
    response.raise_for_status()

    new_block.display_source = upload_data["url"]
    new_block.source = upload_data["url"]
    new_block.file_id = _extract_file_id(upload_data["url"])

    if isinstance(new_block, FileBlock):
        new_block.size = _sizeof_fmt(len(resource.data_bin))
        new_block.title = resource.file_name


def _extract_file_id(url):
    return url[len(S3_URL_PREFIX) :].split("/")[0]


def _sizeof_fmt(num):
    for unit in ("B", "KB", "MB", "GB"):
        if abs(num) < 1024:
            if unit == "B":
                return f"{num}{unit}"
            return f"{num:3.1f}{unit}"
        num /= 1024.0
    return f"{num:.1f}TB"
