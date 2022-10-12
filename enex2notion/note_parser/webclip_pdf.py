import hashlib
import logging
import re
from base64 import b64encode

import fitz
import pdfkit
from bs4 import Tag

from enex2notion.enex_types import EvernoteNote, EvernoteResource
from enex2notion.notion_blocks.uploadable import NotionImageBlock, NotionPDFBlock

logger = logging.getLogger(__name__)


def parse_webclip_to_pdf(note: EvernoteNote, note_dom: Tag, is_add_pdf_preview: bool):
    _convert_local_images(note_dom, note)

    _remove_remote_images(note_dom)

    note_blocks = []

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

    if is_add_pdf_preview:
        note_blocks.append(_get_pdf_preview(pdf_bin))

    pdf_md5 = hashlib.md5(pdf_bin).hexdigest()

    note_blocks.append(
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
    )

    return note_blocks


def _get_pdf_preview(pdf_bin: bytes):
    pix_bin = _get_pdf_first_page_png(pdf_bin)

    pix_md5 = hashlib.md5(pix_bin).hexdigest()

    return NotionImageBlock(
        md5_hash=pix_md5,
        resource=EvernoteResource(
            data_bin=pix_bin,
            size=len(pix_bin),
            md5=pix_md5,
            mime="image/png",
            file_name=f"{pix_md5}.png",
        ),
    )


def _get_pdf_first_page_png(pdf_bin: bytes):  # pragma: no cover
    doc = fitz.open("pdf", pdf_bin)
    page = doc.load_page(0)
    pix = page.get_pixmap()
    return pix.tobytes()


def _convert_local_images(note_dom: Tag, note: EvernoteNote):
    images = note_dom.find_all("en-media")

    for image in images:
        resource = note.resource_by_md5(image.get("hash", "").lower())
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
