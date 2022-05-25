from bs4 import NavigableString, Tag

from enex2notion.note_parser.webclip_stages_common import rename_tags


def convert_paragraphs(root: Tag):
    paragraph_blocks = [
        "address",
        "pre",
        "p",
        "blockquote",
        "dl",
        "dt",
    ]

    rename_tags(root, paragraph_blocks, "div")


def convert_subheaders(root: Tag):
    rename_tags(root, ["h4", "h5", "h6"], "h3")


def convert_inline_modifiers(root: Tag):
    rename_tags(root, ["strong"], "b")

    rename_tags(root, ["em", "cite", "dfn", "abbr", "acronym"], "i")

    rename_tags(root, ["strike", "del"], "s")


def convert_textless_links(root: Tag):
    for e in root.find_all("a"):
        if not e.text.strip() and e.get("href"):
            whitespace = (s for s in e.children if isinstance(s, NavigableString))
            for w in whitespace:
                w.extract()

            e.append(e["href"])


def convert_newlines(root: Tag):
    for e in root.find_all("br"):
        e.replace_with("\n")
