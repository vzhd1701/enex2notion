from bs4 import Tag

from enex2notion.notion_blocks import TextProp
from enex2notion.string_extractor_properties import resolve_string_properties


def extract_string(tag: Tag) -> TextProp:
    """Convert a block content into a string with properties

     IN: <div>some text <b>bold <i>bold and italic</i></b></div>
    OUT: some text bold bold and italic
         [["some text "], ["bold ", ["b"]], ["bold and italic", ["b", "i"]]]
    """

    # Element is either a single div itself or a collection of div or h1-3 "lines"#
    div_lines = tag.find_all(["h1", "h2", "h3", "div"]) or [tag]

    string_blocks = _extract_blocks(div_lines)

    result_properties, result_string = _format_blocks(string_blocks)

    return TextProp(result_string, result_properties)


def _extract_blocks(div_lines):
    """Get parent stack for each string in the line and convert them to properties

    IN: <div>some text <b>bold</b></div>
    OUT: [
            {"string": "some text", "properties": set()},
            {"string": "bold", "properties": {("b",)}},
         ]
    """

    string_blocks = []
    for div in div_lines:
        for string in div.strings:
            parent_stack = _parents_upto(string, div)
            string_properties = resolve_string_properties(parent_stack)

            _add_string_block(string_blocks, string, string_properties)

        # Add linebreak after each "line"
        # to render embedded lists in tables
        # skip last to avoid trailing linebreak
        if div != div_lines[-1]:
            _add_string_block(string_blocks, "\n", set())
    return string_blocks


def _parents_upto(tag: Tag, upto: Tag):
    parents = []
    for p in tag.parents:
        parents.append(p)
        if p == upto:
            break
    return parents


def _add_string_block(string_blocks, string, string_properties):
    if string_blocks and string_blocks[-1]["properties"] == string_properties:
        string_blocks[-1]["string"] += str(string)
    else:
        string_blocks.append({"string": str(string), "properties": string_properties})


def _format_blocks(string_blocks):
    """Notion properties format:

    plain text: ["some text"]
    formatted text: ["some text", ["property"]]
    multiple properties: ["some text", ["property1", "property2"]]
    property with args: ["some text", [["property", "arg"]]]
    """

    result_properties = []
    for block in string_blocks:
        if block["properties"]:
            properties = [list(p) for p in block["properties"]]
            properties.sort(key=lambda p: "".join(p))

            result_properties.append([block["string"], properties])
        else:
            result_properties.append([block["string"]])
    result_string = "".join(b["string"] for b in string_blocks)

    return result_properties, result_string
