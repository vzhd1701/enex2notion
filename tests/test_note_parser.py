import base64
import logging
from datetime import datetime

import pytest
from dateutil.tz import tzutc

from enex2notion.enex_types import EvernoteNote, EvernoteResource
from enex2notion.note_parser.blocks import parse_note_blocks
from enex2notion.note_parser.note import parse_note
from enex2notion.notion_blocks.container import NotionCalloutBlock, NotionCodeBlock
from enex2notion.notion_blocks.embeddable import NotionImageEmbedBlock
from enex2notion.notion_blocks.header import (
    NotionHeaderBlock,
    NotionSubheaderBlock,
    NotionSubsubheaderBlock,
)
from enex2notion.notion_blocks.list import (
    NotionBulletedListBlock,
    NotionNumberedListBlock,
    NotionTodoBlock,
)
from enex2notion.notion_blocks.minor import NotionBookmarkBlock, NotionDividerBlock
from enex2notion.notion_blocks.text import NotionTextBlock, TextProp
from enex2notion.notion_blocks.uploadable import (
    NotionAudioBlock,
    NotionFileBlock,
    NotionImageBlock,
    NotionPDFBlock,
    NotionVideoBlock,
)


@pytest.mark.parametrize(
    "header_line,expected",
    [
        ("<h1>test1</h1>", NotionHeaderBlock(text_prop=TextProp("test1"))),
        ("<h2>test2</h2>", NotionSubheaderBlock(text_prop=TextProp("test2"))),
        ("<h3>test3</h3>", NotionSubsubheaderBlock(text_prop=TextProp("test3"))),
    ],
)
def test_header(header_line, expected, parse_html):
    test_note = parse_html(header_line)

    assert parse_note_blocks(test_note) == [expected]


def test_divider(parse_html):
    test_note = parse_html("<hr/>")

    assert parse_note_blocks(test_note) == [NotionDividerBlock()]


def test_list_ul(parse_html):
    test_note = parse_html("<ul><li><div>test</div></li></ul>")

    assert parse_note_blocks(test_note) == [
        NotionBulletedListBlock(text_prop=TextProp("test"))
    ]


def test_list_ul_ul(parse_html):
    test_note = parse_html(
        "<ul><ul><li><div>test_sub</div></li></ul><li><div>test</div></li></ul>"
    )

    expected = [
        NotionBulletedListBlock(text_prop=TextProp(text="")),
        NotionBulletedListBlock(text_prop=TextProp("test")),
    ]
    expected[0].children = [NotionBulletedListBlock(text_prop=TextProp("test_sub"))]

    assert parse_note_blocks(test_note) == expected


def test_list_ol_ol(parse_html):
    test_note = parse_html(
        "<ol><ol><li><div>test_sub</div></li></ol><li><div>test</div></li></ol>"
    )

    expected = [
        NotionNumberedListBlock(text_prop=TextProp(text="")),
        NotionNumberedListBlock(text_prop=TextProp("test")),
    ]
    expected[0].children = [NotionNumberedListBlock(text_prop=TextProp("test_sub"))]

    assert parse_note_blocks(test_note) == expected


def test_list_ul_todo(parse_html):
    test_note = parse_html(
        (
            "<ul>"
            '<li><div><en-todo checked="true" />test1</div></li>'
            '<li><div><en-todo checked="false" />test2</div></li>'
            "</ul>"
        )
    )

    assert parse_note_blocks(test_note) == [
        NotionTodoBlock(text_prop=TextProp("test1"), checked=True),
        NotionTodoBlock(text_prop=TextProp("test2"), checked=False),
    ]


def test_list_ol(parse_html):
    test_note = parse_html("<ol><li><div>test</div></li></ol>")

    assert parse_note_blocks(test_note) == [
        NotionNumberedListBlock(text_prop=TextProp("test"))
    ]


def test_list_ul_nested(parse_html):
    test_note = parse_html(
        (
            "<ul>"
            " <li><div>test1</div></li>"
            " <ul>"
            "  <li><div>test2</div></li>"
            " </ul>"
            " <ol>"
            "  <li><div>test3</div></li>"
            " </ol>"
            " <li><div>test4</div></li>"
            "</ul>"
        )
    )

    expected = [
        NotionBulletedListBlock(text_prop=TextProp("test1")),
        NotionBulletedListBlock(text_prop=TextProp("test4")),
    ]
    expected[0].children = [
        NotionBulletedListBlock(text_prop=TextProp("test2")),
        NotionNumberedListBlock(text_prop=TextProp("test3")),
    ]

    assert parse_note_blocks(test_note) == expected


def test_list_ul_images_inside(parse_html, caplog):
    test_note = parse_html(
        "<ul>"
        "<li>"
        "<div>test1</div>"
        '<en-media type="image/png" hash="fake_hash" />'
        '<img src="https://google.com/image.jpg" />'
        "</li>"
        "</ul>"
    )

    expected_block = NotionBulletedListBlock(text_prop=TextProp("test1"))
    expected_block.children = [
        NotionImageBlock(md5_hash="fake_hash"),
        NotionImageEmbedBlock(url="https://google.com/image.jpg"),
    ]

    assert parse_note_blocks(test_note) == [expected_block]


def test_list_ul_strings_inside(parse_html, caplog):
    test_note = parse_html("<ul><li><div>test1</div></li>test2</ul>")

    with caplog.at_level(logging.DEBUG, logger="enex2notion"):
        result_blocks = parse_note_blocks(test_note)

    assert "Non-empty string element inside list" in caplog.text
    assert result_blocks == [
        NotionBulletedListBlock(text_prop=TextProp("test1")),
        NotionTextBlock(text_prop=TextProp("test2")),
    ]


def test_list_ul_unexpected_inside(parse_html, caplog):
    test_note = parse_html("<ul><li><div>test1</div></li><span>test2</span></ul>")

    with caplog.at_level(logging.DEBUG, logger="enex2notion"):
        result_blocks = parse_note_blocks(test_note)

    assert "Unexpected tag inside list" in caplog.text
    assert result_blocks == [
        NotionBulletedListBlock(text_prop=TextProp("test1")),
        NotionTextBlock(text_prop=TextProp("test2")),
    ]


def test_table(parse_html):
    test_note = parse_html(
        "<table>"
        "<tr><td>test1</td><td>test2</td><td>test3</td></tr>"
        "<tr><td>test4</td><td>test5</td><td>test6</td></tr>"
        "<tr><td>test7</td><td>test8</td><td>test9</td></tr>"
        "</table>"
    )

    table = parse_note_blocks(test_note)[0]

    assert len(table.children) == 3
    assert list(table.iter_rows()) == [
        [
            TextProp("test1").properties,
            TextProp("test2").properties,
            TextProp("test3").properties,
        ],
        [
            TextProp("test4").properties,
            TextProp("test5").properties,
            TextProp("test6").properties,
        ],
        [
            TextProp("test7").properties,
            TextProp("test8").properties,
            TextProp("test9").properties,
        ],
    ]


def test_table_padded(parse_html):
    test_note = parse_html(
        "<table>"
        '<tr><td colspan="2">test1</td></tr>'
        "<tr><td>test2</td><td>test3</td></tr>"
        "</table>"
    )

    table = parse_note_blocks(test_note)[0]
    assert len(table.children) == 2
    assert list(table.iter_rows()) == [
        [
            TextProp("test1").properties,
            TextProp("").properties,
        ],
        [
            TextProp("test2").properties,
            TextProp("test3").properties,
        ],
    ]


def test_table_empty(parse_html):
    test_note = parse_html("<table></table>")

    assert parse_note_blocks(test_note) == []


@pytest.mark.parametrize(
    "mime, expected_block",
    [
        ("image/png", NotionImageBlock),
        ("video/mp4", NotionVideoBlock),
        ("audio/mp4", NotionAudioBlock),
        ("application/pdf", NotionPDFBlock),
        ("application/octet-stream", NotionFileBlock),
    ],
)
def test_embedded_media(mime, expected_block, parse_html):
    test_note = parse_html(f'<en-media type="{mime}" hash="test" />')

    assert parse_note_blocks(test_note) == [expected_block(md5_hash="test")]


def test_embedded_media_with_dimensions_old_style(parse_html):
    test_note = parse_html(
        '<en-media type="image/png" width=100 height=200 hash="test" />'
    )

    assert parse_note_blocks(test_note) == [
        NotionImageBlock(md5_hash="test", width=100, height=200)
    ]


def test_embedded_media_svg_no_size(parse_html):
    test_note = parse_html('<en-media type="image/svg+xml" hash="test" />')

    assert parse_note_blocks(test_note) == [
        NotionImageBlock(md5_hash="test", width=50, height=50)
    ]


def test_embedded_inline_img_bin(parse_html, smallest_gif):
    test_note = parse_html(
        f'<img width="100px" '
        f'src="data:{smallest_gif.mime};'
        f'base64,{base64.b64encode(smallest_gif.data_bin).decode("utf-8")}" />'
    )

    result_block = parse_note_blocks(test_note)[0]

    assert result_block == NotionImageBlock(
        md5_hash=smallest_gif.md5,
        width=100,
        resource=EvernoteResource(
            data_bin=smallest_gif.data_bin,
            size=smallest_gif.size,
            md5=smallest_gif.md5,
            mime=smallest_gif.mime,
            file_name=f"{smallest_gif.md5}.gif",
        ),
    )
    assert result_block.width == 100
    assert result_block.height is None


def test_embedded_inline_img_svg(parse_html, smallest_svg):
    test_note = parse_html(
        f'<img width="100px" '
        f'src="data:{smallest_svg.mime},'
        f'{smallest_svg.data_bin.decode("utf-8")}" />'
    )

    result_block = parse_note_blocks(test_note)[0]

    assert result_block == NotionImageBlock(
        md5_hash=smallest_svg.md5,
        width=100,
        resource=EvernoteResource(
            data_bin=smallest_svg.data_bin,
            size=smallest_svg.size,
            md5=smallest_svg.md5,
            mime=smallest_svg.mime,
            file_name=f"{smallest_svg.md5}.svg",
        ),
    )
    assert result_block.width == 100
    assert result_block.height is None


def test_embedded_inline_svg_no_size(parse_html, smallest_svg):
    test_note = parse_html(
        f"<img "
        f'src="data:{smallest_svg.mime},'
        f'{smallest_svg.data_bin.decode("utf-8")}" />'
    )

    result_block = parse_note_blocks(test_note)[0]

    assert result_block == NotionImageBlock(
        md5_hash=smallest_svg.md5,
        height=50,
        width=50,
        resource=EvernoteResource(
            data_bin=smallest_svg.data_bin,
            size=smallest_svg.size,
            md5=smallest_svg.md5,
            mime=smallest_svg.mime,
            file_name=f"{smallest_svg.md5}.svg",
        ),
    )


def test_embedded_inline_bad(parse_html, smallest_svg, caplog):
    test_note = parse_html(
        f"<img "
        'src="data:image/svg+xml;utf8,'
        "<svg xmlns='http://www.w3.org/2000/svg' width='416' height='377'>"
        '</svg/>" />'
    )

    with caplog.at_level(logging.WARNING, logger="enex2notion"):
        result_block = parse_note_blocks(test_note)

    assert result_block == []
    assert "Failed to parse image" in caplog.text


def test_embedded_inline_img_url(parse_html):
    test_note = parse_html('<img src="https://google.com/image.jpg" />')

    result_block = parse_note_blocks(test_note)[0]

    assert result_block == NotionImageEmbedBlock(url="https://google.com/image.jpg")
    assert result_block.source_url == "https://google.com/image.jpg"


def test_embedded_link(parse_html):
    test_note = parse_html(
        '<div style="--en-richlink:true;'
        " --en-href:https://google.com;"
        " --en-viewerProps:not_relevant;"
        ' --en-title:file.ext;">'
        '<a href="https://google.com" rev="en_rl_small">file.ext</a>'
        "</div>"
    )

    assert parse_note_blocks(test_note) == [
        NotionBookmarkBlock(url="https://google.com")
    ]


def test_code_block(parse_html):
    test_note = parse_html(
        '<div style="--en-codeblock:true;some_irrelevant_css">'
        " <div>test1</div>"
        " <div>test2</div>"
        "</div>"
    )

    assert parse_note_blocks(test_note) == [
        NotionCodeBlock(text_prop=TextProp("test1\ntest2"))
    ]


def test_indented_complex(parse_html):
    test_note = parse_html(
        "<div>test1</div>"
        '<div style="padding-left:40px;">test2</div>'
        '<div style="padding-left:40px;">test3</div>'
        '<div style="padding-left:80px;">test4</div>'
        '<div style="padding-left:80px;">test5</div>'
        '<div style="padding-left:120px;">test6</div>'
        '<div style="padding-left:40px;">test7</div>'
        "<div>test8</div>"
        "<div>test9</div>"
    )

    expected_result = [
        NotionTextBlock(text_prop=TextProp("test1")),
        NotionTextBlock(text_prop=TextProp("test8")),
        NotionTextBlock(text_prop=TextProp("test9")),
    ]
    expected_result[0].children = [
        NotionTextBlock(text_prop=TextProp("test2")),
        NotionTextBlock(text_prop=TextProp("test3")),
        NotionTextBlock(text_prop=TextProp("test7")),
    ]
    expected_result[0].children[1].children = [
        NotionTextBlock(text_prop=TextProp("test4")),
        NotionTextBlock(text_prop=TextProp("test5")),
    ]
    expected_result[0].children[1].children[1].children = [
        NotionTextBlock(text_prop=TextProp("test6")),
    ]

    assert parse_note_blocks(test_note) == expected_result


def test_indented(parse_html):
    test_note = parse_html(
        '<div>test1</div><div style="padding-left:40px;">test2</div><div>test3</div>'
    )

    expected_result = [
        NotionTextBlock(text_prop=TextProp("test1")),
        NotionTextBlock(text_prop=TextProp("test3")),
    ]
    expected_result[0].children = [
        NotionTextBlock(text_prop=TextProp("test2")),
    ]

    assert parse_note_blocks(test_note) == expected_result


def test_indented_nested(parse_html):
    test_note = parse_html(
        "<div>test1</div>"
        '<div style="padding-left:40px;">test2</div>'
        '<div style="padding-left:80px;">test3</div>'
        '<div style="padding-left:120px;">test4</div>'
        '<div style="padding-left:160px;">test5</div>'
    )

    expected_result = [
        NotionTextBlock(text_prop=TextProp("test1")),
    ]
    expected_result[0].children = [
        NotionTextBlock(text_prop=TextProp("test2")),
    ]
    expected_result[0].children[0].children = [
        NotionTextBlock(text_prop=TextProp("test3")),
    ]
    expected_result[0].children[0].children[0].children = [
        NotionTextBlock(text_prop=TextProp("test4")),
    ]
    expected_result[0].children[0].children[0].children[0].children = [
        NotionTextBlock(text_prop=TextProp("test5")),
    ]

    assert parse_note_blocks(test_note) == expected_result


def test_indented_from_start(parse_html):
    test_note = parse_html('<div style="padding-left:40px;">test1</div>')

    expected_result = [
        NotionTextBlock(text_prop=TextProp("")),
    ]
    expected_result[0].children = [
        NotionTextBlock(text_prop=TextProp("test1")),
    ]

    assert parse_note_blocks(test_note) == expected_result


def test_indented_messed(parse_html):
    test_note = parse_html(
        "<div>test1</div>"
        '<div style="padding-left:80px;">test2</div>'
        '<div style="padding-left:40px;">test3</div>'
    )

    expected_result = [
        NotionTextBlock(text_prop=TextProp("test1")),
    ]
    expected_result[0].children = [
        NotionTextBlock(text_prop=TextProp("        test2")),
        NotionTextBlock(text_prop=TextProp("    test3")),
    ]

    assert parse_note_blocks(test_note) == expected_result


def test_text_block(parse_html):
    test_note = parse_html("<div>test1</div>")

    assert parse_note_blocks(test_note) == [
        NotionTextBlock(text_prop=TextProp("test1"))
    ]


def test_text_block_todo(parse_html):
    test_note = parse_html(
        '<div><en-todo checked="false" />test1</div>'
        '<div><en-todo checked="true" />test2</div>'
    )

    assert parse_note_blocks(test_note) == [
        NotionTodoBlock(text_prop=TextProp("test1"), checked=False),
        NotionTodoBlock(text_prop=TextProp("test2"), checked=True),
    ]


def test_skipped_blocks(parse_html):
    test_note = parse_html(
        '<div style="--en-task-group:true;">'
        "   <div>irrelevant stuff</div>"
        "</div>"
        "<en-crypt>irrelevant stuff</en-crypt>"
    )

    assert parse_note_blocks(test_note) == []


def test_extracted_blocks(parse_html):
    test_note = parse_html('<div>test <en-media type="image/png" hash="test" /></div>')

    assert parse_note_blocks(test_note) == [
        NotionTextBlock(text_prop=TextProp("test ")),
        NotionImageBlock(md5_hash="test"),
    ]


def test_flattened_root(parse_html):
    test_note = parse_html(
        "<div><div>paragraph1</div><div>paragraph2</div><div><br></div></div>"
    )

    assert parse_note_blocks(test_note) == [
        NotionTextBlock(text_prop=TextProp("paragraph1")),
        NotionTextBlock(text_prop=TextProp("paragraph2")),
        NotionTextBlock(text_prop=TextProp("")),
    ]


def test_flattened_deep_root(parse_html):
    test_note = parse_html(
        "<div><div><div>paragraph1</div><div>paragraph2</div></div><div><br></div></div>"
    )

    assert parse_note_blocks(test_note) == [
        NotionTextBlock(text_prop=TextProp("paragraph1")),
        NotionTextBlock(text_prop=TextProp("paragraph2")),
        NotionTextBlock(text_prop=TextProp("")),
    ]


def test_flattened_div_with_strings(parse_html):
    test_note = parse_html(
        "<div>"
        "<div>paragraph1</div>"
        "subparagraph1"
        "<div>paragraph2</div>"
        "subparagraph2"
        "<div><br></div>"
        "</div>"
    )

    assert parse_note_blocks(test_note) == [
        NotionTextBlock(text_prop=TextProp("paragraph1")),
        NotionTextBlock(text_prop=TextProp("subparagraph1")),
        NotionTextBlock(text_prop=TextProp("paragraph2")),
        NotionTextBlock(text_prop=TextProp("subparagraph2")),
        NotionTextBlock(text_prop=TextProp("")),
    ]


def test_flattened_div_with_strings_at_the_end(parse_html):
    test_note = parse_html("<div><div>paragraph1</div>subparagraph1</div>")

    assert parse_note_blocks(test_note) == [
        NotionTextBlock(text_prop=TextProp("paragraph1")),
        NotionTextBlock(text_prop=TextProp("subparagraph1")),
    ]


def test_flattened_root_empty_divs(parse_html):
    test_note = parse_html("<div><div>paragraph1</div><div></div><div><br></div></div>")

    assert parse_note_blocks(test_note) == [
        NotionTextBlock(text_prop=TextProp("paragraph1")),
        NotionTextBlock(text_prop=TextProp("")),
    ]


def test_extract_embedded(parse_html):
    test_note = parse_html(
        "<div>"
        "<table>"
        "<tr>"
        "<td>test1</td>"
        '<td><en-media type="image/png" hash="test" /></td>'
        "</tr>"
        "</table>"
        "</div>"
    )

    result_blocks = parse_note_blocks(test_note)

    assert len(result_blocks) == 2
    assert result_blocks[1] == NotionImageBlock(md5_hash="test")


def test_unknown_block(parse_html):
    test_note = parse_html("<unknown>test</unknown>")

    assert parse_note_blocks(test_note) == [
        NotionTextBlock(text_prop=TextProp("test")),
    ]


def test_text_inside_root(parse_html):
    test_note = parse_html("texty")

    assert parse_note_blocks(test_note) == [
        NotionTextBlock(text_prop=TextProp("texty")),
    ]


def test_linebreaks_inside_root(parse_html):
    test_note = parse_html("\n<div>texty</div>\n")

    assert parse_note_blocks(test_note) == [
        NotionTextBlock(text_prop=TextProp("texty")),
    ]


def test_empty_note(parse_rules):
    test_note = EvernoteNote(
        title="test1",
        created=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        updated=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        content="<en-note></en-note>",
        tags=[],
        author="",
        url="",
        is_webclip=False,
        resources=[],
    )

    assert parse_note(test_note, parse_rules) == []


def test_yinxiang_markdown(parse_rules):
    test_note = EvernoteNote(
        title="test1",
        created=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        updated=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        content=(
            "<en-note>"
            "<div>test1</div>"
            "<center style='display:none'>test2</center>"
            "</en-note>"
        ),
        tags=[],
        author="",
        url="",
        is_webclip=False,
        resources=[],
    )

    assert parse_note(test_note, parse_rules) == [
        NotionTextBlock(text_prop=TextProp("test1")),
    ]


def test_yinxiang_markdown_bad_end(parse_rules):
    test_note = EvernoteNote(
        title="test1",
        created=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        updated=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        content=("<en-note><div>test1</div>\n</en-note>"),
        tags=[],
        author="",
        url="",
        is_webclip=False,
        resources=[],
    )

    assert parse_note(test_note, parse_rules) == [
        NotionTextBlock(text_prop=TextProp("test1")),
    ]


def test_resource_recursive(smallest_gif, parse_rules):
    test_note = EvernoteNote(
        title="test1",
        created=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        updated=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        content=(
            "<en-note>"
            "<ul><li>"
            f'<en-media type="{smallest_gif.mime}" hash="{smallest_gif.md5}" />'
            "</li></ul>"
            "</en-note>"
        ),
        tags=[],
        author="",
        url="",
        is_webclip=False,
        resources=[smallest_gif],
    )

    test_embedded_image = parse_note(test_note, parse_rules)[0].children[0]

    assert test_embedded_image == NotionImageBlock(
        md5_hash=smallest_gif.md5, resource=smallest_gif
    )


def test_resource_hash_case(smallest_gif, parse_rules):
    test_note = EvernoteNote(
        title="test1",
        created=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        updated=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        content=(
            "<en-note>"
            "<ul><li>"
            f'<en-media type="{smallest_gif.mime}" hash="{smallest_gif.md5.upper()}" />'
            "</li></ul>"
            "</en-note>"
        ),
        tags=[],
        author="",
        url="",
        is_webclip=False,
        resources=[smallest_gif],
    )

    test_embedded_image = parse_note(test_note, parse_rules)[0].children[0]

    assert test_embedded_image == NotionImageBlock(
        md5_hash=smallest_gif.md5, resource=smallest_gif
    )


def test_bad_resource(caplog, parse_rules):
    test_note = EvernoteNote(
        title="test1",
        created=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        updated=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        content='<en-note><en-media type="fake/mime" hash="fake_hash" /></en-note>',
        tags=[],
        author="",
        url="",
        is_webclip=False,
        resources=[],
    )

    with caplog.at_level(logging.DEBUG, logger="enex2notion"):
        result_blocks = parse_note(test_note, parse_rules)

    assert "Failed to resolve resource" in caplog.text
    assert result_blocks == []


def test_bad_note(caplog, parse_rules):
    test_note = EvernoteNote(
        title="test1",
        created=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        updated=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        content="bad",
        tags=[],
        author="",
        url="",
        is_webclip=False,
        resources=[],
    )

    with caplog.at_level(logging.ERROR, logger="enex2notion"):
        result_blocks = parse_note(test_note, parse_rules)

    assert "Failed to extract" in caplog.text
    assert result_blocks == []


def test_note_with_meta(parse_rules):
    test_note = EvernoteNote(
        title="test1",
        created=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        updated=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        content="<en-note><div>test</div></en-note>",
        tags=["tag1", "tag2"],
        author="",
        url="https://google.com",
        is_webclip=False,
        resources=[],
    )

    expected_meta = (
        "Created: 2021-11-18T00:00:00+00:00\n"
        "Updated: 2021-11-18T00:00:00+00:00\n"
        "URL: https://google.com\n"
        "Tags: tag1, tag2"
    )

    parse_rules.add_meta = True

    fake_note_blocks = parse_note(test_note, parse_rules)

    assert fake_note_blocks == [
        NotionCalloutBlock(
            icon="ℹ️",
            text_prop=TextProp(text=expected_meta),
        ),
        NotionTextBlock(text_prop=TextProp("test")),
    ]


def test_note_webclip(parse_rules):
    test_note = EvernoteNote(
        title="test1",
        created=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        updated=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        content="<en-note><div>test</div></en-note>",
        tags=[],
        author="",
        url="",
        is_webclip=True,
        resources=[],
    )

    fake_note_blocks = parse_note(test_note, parse_rules)

    assert fake_note_blocks == [
        NotionTextBlock(text_prop=TextProp("test")),
    ]


def test_condense_lines_empty_divide(parse_rules):
    test_note = EvernoteNote(
        title="test1",
        created=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        updated=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        content=(
            "<en-note>"
            "<div>test1</div>"
            "<div>test2</div>"
            "<div><br /></div>"
            "<div>test3</div>"
            "<div>test4</div>"
            "</en-note>"
        ),
        tags=[],
        author="",
        url="",
        is_webclip=False,
        resources=[],
    )

    parse_rules.condense_lines = True

    fake_note_blocks = parse_note(test_note, parse_rules)

    assert fake_note_blocks == [
        NotionTextBlock(
            text_prop=TextProp(
                text="test1\ntest2", properties=[["test1"], ["\n"], ["test2"]]
            )
        ),
        NotionTextBlock(
            text_prop=TextProp(
                text="test3\ntest4", properties=[["test3"], ["\n"], ["test4"]]
            )
        ),
    ]


def test_condense_lines_trailing_divide(parse_rules):
    test_note = EvernoteNote(
        title="test1",
        created=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        updated=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        content=(
            "<en-note>"
            "<div>test1</div>"
            "<div>test2</div>"
            "<div><br /></div>"
            "<div><br /></div>"
            "<div>test3</div>"
            "<div>test4</div>"
            "<div><br /></div>"
            "</en-note>"
        ),
        tags=[],
        author="",
        url="",
        is_webclip=False,
        resources=[],
    )

    parse_rules.condense_lines = True

    fake_note_blocks = parse_note(test_note, parse_rules)

    assert fake_note_blocks == [
        NotionTextBlock(
            text_prop=TextProp(
                text="test1\ntest2", properties=[["test1"], ["\n"], ["test2"]]
            )
        ),
        NotionTextBlock(
            text_prop=TextProp(
                text="test3\ntest4", properties=[["test3"], ["\n"], ["test4"]]
            )
        ),
    ]


def test_condense_lines_sparse(parse_rules):
    test_note = EvernoteNote(
        title="test1",
        created=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        updated=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        content=(
            "<en-note>"
            "<div>test1</div>"
            "<div>test2</div>"
            "<div><br /></div>"
            "<div><br /></div>"
            "<div>test3</div>"
            "<div>test4</div>"
            "<div><br /></div>"
            "</en-note>"
        ),
        tags=[],
        author="",
        url="",
        is_webclip=False,
        resources=[],
    )

    parse_rules.condense_lines_sparse = True

    fake_note_blocks = parse_note(test_note, parse_rules)

    assert fake_note_blocks == [
        NotionTextBlock(
            text_prop=TextProp(
                text="test1\ntest2", properties=[["test1"], ["\n"], ["test2"]]
            )
        ),
        NotionTextBlock(),
        NotionTextBlock(
            text_prop=TextProp(
                text="test3\ntest4", properties=[["test3"], ["\n"], ["test4"]]
            )
        ),
    ]


def test_condense_lines_non_text_block(parse_rules):
    test_note = EvernoteNote(
        title="test1",
        created=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        updated=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        content=(
            "<en-note>"
            "<div>test1</div>"
            "<div>test2</div>"
            "<h1>Test</h1>"
            "<div>test3</div>"
            "<div>test4</div>"
            "</en-note>"
        ),
        tags=[],
        author="",
        url="",
        is_webclip=False,
        resources=[],
    )

    parse_rules.condense_lines = True

    fake_note_blocks = parse_note(test_note, parse_rules)

    assert fake_note_blocks == [
        NotionTextBlock(
            text_prop=TextProp(
                text="test1\ntest2", properties=[["test1"], ["\n"], ["test2"]]
            )
        ),
        NotionHeaderBlock(text_prop=TextProp("Test")),
        NotionTextBlock(
            text_prop=TextProp(
                text="test3\ntest4", properties=[["test3"], ["\n"], ["test4"]]
            )
        ),
    ]


def test_condense_lines_children(parse_rules):
    test_note = EvernoteNote(
        title="test1",
        created=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        updated=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        content=(
            "<en-note>"
            "<div>test1</div>"
            "<div>test2</div>"
            '<div style="padding-left:40px;">test3</div>'
            '<div style="padding-left:40px;">test4</div>'
            "<div>test5</div>"
            "<div>test6</div>"
            "</en-note>"
        ),
        tags=[],
        author="",
        url="",
        is_webclip=False,
        resources=[],
    )

    parse_rules.condense_lines = True

    fake_note_blocks = parse_note(test_note, parse_rules)

    expected_note_blocks = [
        NotionTextBlock(
            text_prop=TextProp(
                text="test1\ntest2", properties=[["test1"], ["\n"], ["test2"]]
            )
        ),
        NotionTextBlock(
            text_prop=TextProp(
                text="test5\ntest6", properties=[["test5"], ["\n"], ["test6"]]
            )
        ),
    ]
    expected_note_blocks[0].children = [
        NotionTextBlock(
            text_prop=TextProp(
                text="test3\ntest4", properties=[["test3"], ["\n"], ["test4"]]
            )
        )
    ]

    assert fake_note_blocks == expected_note_blocks


def test_text_prop_strip():
    test_text_prop = TextProp(text="\ntest1\n", properties=[["\ntest1\n"]])

    trimmed_text_prop = test_text_prop.strip()

    assert trimmed_text_prop.text == "test1"
    assert trimmed_text_prop.properties == [["test1"]]


def test_text_prop_strip_empty_ends():
    test_text_prop = TextProp(text="\ntest1\n", properties=[["\n"], ["test1"], ["\n"]])

    trimmed_text_prop = test_text_prop.strip()

    assert trimmed_text_prop.text == "test1"
    assert trimmed_text_prop.properties == [["test1"]]


def test_text_prop_strip_props():
    test_text_prop = TextProp(
        text="\n1\ntest1\ntest2\n\n2\n",
        properties=[["\n1\n", [["b"]]], ["test1"], ["\ntest2\n"], ["\n2\n", [["b"]]]],
    )

    trimmed_text_prop = test_text_prop.strip()

    assert trimmed_text_prop.text == "1\ntest1\ntest2\n\n2"
    assert trimmed_text_prop.properties == [
        ["1\n", [["b"]]],
        ["test1"],
        ["\ntest2\n"],
        ["\n2", [["b"]]],
    ]
