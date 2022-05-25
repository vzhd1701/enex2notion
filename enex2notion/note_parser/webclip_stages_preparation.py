from bs4 import Tag

from enex2notion.note_parser.webclip_stages_common import rename_tags


def remove_unprocessable(root: Tag):
    for e in root.find_all(["nav", "menu"]):
        e.extract()


def unpack_block_elements(root: Tag):
    container_blocks = [
        "main",
        "section",
        "article",
        "aside",
        "fieldset",
        "form",
        "details",
        "dialog",
        "dd",
        "hgroup",
        "figure",
        "footer",
        "header",
    ]

    for b in container_blocks:
        for e in root.find_all(b):
            e.insert_after(*e.contents)
            e.extract()


def unpack_tables(root: Tag):
    for cg in root.find_all("colgroup"):
        cg.decompose()

    for b in ("tr", "thead", "tbody", "tfoot", "table"):
        for e in root.find_all(b):
            e.insert_after(*e.contents)
            e.extract()

    rename_tags(root, ["caption", "td", "th"], "div")
