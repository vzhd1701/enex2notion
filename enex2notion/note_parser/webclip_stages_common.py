from bs4 import Tag

BLOCK_TAGS = (
    "div",
    "h1",
    "h2",
    "h3",
    "hr",
    "ul",
    "ol",
    "en-media",
    "img",
)
STANDALONE_TAGS = ("en-media", "img", "ol", "ul", "hr")


def rename_tags(root: Tag, tags_to_rename: list, new_name: str):
    for e in root.find_all(tags_to_rename):
        e.name = new_name
