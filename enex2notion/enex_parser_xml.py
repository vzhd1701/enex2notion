from collections import defaultdict
from pathlib import Path
from typing import Any, Callable, Dict, Iterator, List, Optional

from lxml import etree
from lxml.etree import XMLSyntaxError, _Entity


def iter_xml_elements_as_dict(
    xml_file: Path, tag_name: str
) -> Iterator[Dict[str, Any]]:
    yield from iter_process_xml_elements(
        xml_file, tag_name, lambda e: _etree_to_dict(e)[tag_name]
    )


def iter_process_xml_elements(
    xml_file: Path,
    tag_name: str,
    element_callback: Callable[[Any], Any],
    error_callback: Optional[Callable[[Path, List[str]], None]] = None,
) -> Iterator[Dict[str, Any]]:
    with open(xml_file, "rb") as f:
        context = etree.iterparse(
            f,
            events=("start", "end"),
            recover=True,
            strip_cdata=False,
            resolve_entities=False,
        )

        try:
            _, root = next(context)

            for event, elem in context:
                if event == "end" and elem.tag == tag_name:
                    yield element_callback(elem)

                root.clear()
        except XMLSyntaxError:
            pass
        except Exception as e:
            raise RuntimeError(f"Failed to parse {xml_file.name}") from e

        errors = _format_error_list(xml_file.name, context.error_log)
        if errors and error_callback:
            error_callback(xml_file, errors)


# https://stackoverflow.com/a/10077069/13100286
def _etree_to_dict(t) -> Dict[str, Any]:  # noqa: WPS210, WPS231, C901
    d = {t.tag: {} if t.attrib else None}

    children = list(c for c in t if not isinstance(c, _Entity))
    children_entities = list(c for c in t if isinstance(c, _Entity))

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
            (f"@{k}", v) for k, v in t.attrib.items()
        )  # noqa: WPS221, WPS441

    if t.text or children_entities:
        text = "".join([t.text or "", *_iter_entities_text(children_entities)]).strip()
        if children or t.attrib:
            if text:
                d[t.tag]["#text"] = text
        else:
            d[t.tag] = text

    return d


def _iter_entities_text(entities):
    for e in entities:
        yield _handle_bad_unicode_attr(e, "text")
        yield _handle_bad_unicode_attr(e, "tail")


def _handle_bad_unicode_attr(obj, attr):
    try:
        return getattr(obj, attr)
    except UnicodeDecodeError as e:
        return e.object.decode("utf-8", "ignore")
    except:  # pragma: no cover
        return ""


def _format_error_list(file_name, error_log) -> List[str]:
    return [f"{file_name}:{e.line}:{e.column}:{e.message}" for e in error_log]
