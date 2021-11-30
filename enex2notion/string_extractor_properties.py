import re
from typing import List

from bs4 import Tag

from enex2notion.colors import extract_color


def resolve_string_properties(tags: List[Tag]):
    properties = set()

    tag_map = {
        "b": lambda e: ("b",),
        "i": lambda e: ("i",),
        "u": lambda e: ("_",),
        "s": lambda e: ("s",),
        "span": _resolve_span,
        "a": _resolve_link,
    }

    for tag in tags:
        if tag_map.get(tag.name):
            tag_property = tag_map[tag.name](tag)

            if tag_property:
                if isinstance(tag_property, list):
                    properties.update(tag_property)
                else:
                    properties.add(tag_property)

    return properties


def _resolve_span(tag: Tag):
    properties = []

    style = tag.get("style")
    if not style:
        return []

    color = extract_color(style)
    if color is not None:
        properties.append(("h", color))

    if re.match(r".*font-weight:\s*bold", style):
        properties.append(("b",))

    if re.match(r".*font-style:\s*italic", style):
        properties.append(("i",))

    return properties


def _resolve_link(tag: Tag):
    # TODO: resolve using note title or link list
    if tag.get("href") and "evernote://" not in tag.get("href"):
        return "a", tag["href"]
    return None
