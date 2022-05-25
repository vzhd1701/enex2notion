from collections import defaultdict
from pathlib import Path
from typing import Any, Callable, Dict, Iterator
from xml.etree import ElementTree


def iter_xml_elements_as_dict(
    xml_file: Path, tag_name: str
) -> Iterator[Dict[str, Any]]:
    yield from iter_process_xml_elements(
        xml_file, tag_name, lambda e: _etree_to_dict(e)[tag_name]
    )


def iter_process_xml_elements(
    xml_file: Path, tag_name: str, handler_func: Callable[[Any], Any]
) -> Iterator[Dict[str, Any]]:
    with open(xml_file, "rb") as f:
        context = ElementTree.iterparse(f, events=("start", "end"))

        _, root = next(context)

        for event, elem in context:
            if event == "end" and elem.tag == tag_name:
                yield handler_func(elem)

            root.clear()


# https://stackoverflow.com/a/10077069/13100286
def _etree_to_dict(  # noqa: WPS210, WPS231, C901
    t: ElementTree.Element,
) -> Dict[str, Any]:
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(_etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {
            t.tag: {
                k: v[0] if len(v) == 1 else v  # noqa: WPS441
                for k, v in dd.items()  # noqa: WPS221
            }
        }
    if t.attrib:
        d[t.tag].update(
            (f"@{k}", v) for k, v in t.attrib.items()  # noqa: WPS221, WPS441
        )
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]["#text"] = text
        else:
            d[t.tag] = text
    return d
