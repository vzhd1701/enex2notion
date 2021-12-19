import hashlib
import logging
import re
from base64 import b64encode

import pdfkit
from bs4 import Tag

from enex2notion.enex_types import EvernoteNote, EvernoteResource
from enex2notion.notion_blocks_uploadable import NotionPDFBlock

logger = logging.getLogger(__name__)


def parse_webclip_to_pdf(note: EvernoteNote, note_dom: Tag):
    _convert_local_images(note_dom, note)

    _remove_remote_images(note_dom)

    pdf_bin = pdfkit.from_string(
        str(note_dom),
        options={
            "encoding": "UTF-8",
            "margin-top": "0",
            "margin-right": "0",
            "margin-bottom": "0",
            "margin-left": "0",
        },
    )

    pdf_md5 = hashlib.md5(pdf_bin).hexdigest()

    return [
        NotionPDFBlock(
            md5_hash=pdf_md5,
            resource=EvernoteResource(
                data_bin=pdf_bin,
                size=len(pdf_bin),
                md5=pdf_md5,
                mime="application/pdf",
                file_name=f"{pdf_md5}.pdf",
            ),
        )
    ]


def _convert_local_images(note_dom: Tag, note: EvernoteNote):
    images = note_dom.find_all("en-media")

    for image in images:
        resource = note.resource_by_md5(image.get("hash", ""))
        if resource is None:
            image.decompose()
            continue

        img = Tag(name="img")

        img["src"] = "data:{0};base64,{1}".format(
            resource.mime, b64encode(resource.data_bin).decode("utf-8")
        )

        if image.get("width"):
            img["width"] = image.get("width")
        if image.get("height"):
            img["height"] = image.get("height")

        image.replace_with(img)


def _remove_remote_images(note_dom: Tag):
    for img in note_dom.find_all("img"):
        if not img.get("src", "").startswith("data:"):
            img.decompose()

    elements_with_css_images = note_dom.find_all(style=re.compile(r"url\(http.*?\)"))

    for element in elements_with_css_images:
        element["style"] = re.sub(r"url\(http.*?\)", "", element["style"])
