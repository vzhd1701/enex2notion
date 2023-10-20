import base64

from enex2notion.enex_types import EvernoteResource
from enex2notion.note_parser.webclip import parse_webclip
from enex2notion.notion_blocks.header import NotionSubsubheaderBlock
from enex2notion.notion_blocks.list import NotionBulletedListBlock
from enex2notion.notion_blocks.text import NotionTextBlock, TextProp
from enex2notion.notion_blocks.uploadable import NotionImageBlock


def test_empty(parse_html):
    test_note = parse_html("")

    assert parse_webclip(test_note) == []


def test_invisible_blocks(parse_html):
    test_note = parse_html("<nav>test</nav><menu>test</menu>")

    assert parse_webclip(test_note) == []


def test_table(parse_html):
    test_note = parse_html(
        "<table>"
        "<colgroup><col></colgroup>"
        "<caption>test1</caption>"
        "<thead><tr><th>test2</th></tr></thead>"
        "<tbody><tr><td>test3</td></tr></tbody>"
        "<tfoot><tr><td>test4</td></tr></tfoot>"
        "</table>"
    )

    assert parse_webclip(test_note) == [
        NotionTextBlock(text_prop=TextProp("test1")),
        NotionTextBlock(text_prop=TextProp("test2")),
        NotionTextBlock(text_prop=TextProp("test3")),
        NotionTextBlock(text_prop=TextProp("test4")),
    ]


def test_container_blocks(parse_html):
    test_note = parse_html(
        "<main><div>test1</div></main>"
        "<section><div>test2</div></section>"
        "<article><div>test3</div></article>"
        "<aside><div>test4</div></aside>"
        "<fieldset><div>test5</div></fieldset>"
        "<form><div>test6</div></form>"
        "<details><div>test7</div></details>"
        "<dialog><div>test8</div></dialog>"
        "<dd><div>test9</div></dd>"
        "<hgroup><div>test10</div></hgroup>"
        "<figure><div>test11</div></figure>"
        "<footer><div>test12</div></footer>"
        "<header><div>test13</div></header>"
    )

    assert parse_webclip(test_note) == [
        NotionTextBlock(text_prop=TextProp("test1")),
        NotionTextBlock(text_prop=TextProp("test2")),
        NotionTextBlock(text_prop=TextProp("test3")),
        NotionTextBlock(text_prop=TextProp("test4")),
        NotionTextBlock(text_prop=TextProp("test5")),
        NotionTextBlock(text_prop=TextProp("test6")),
        NotionTextBlock(text_prop=TextProp("test7")),
        NotionTextBlock(text_prop=TextProp("test8")),
        NotionTextBlock(text_prop=TextProp("test9")),
        NotionTextBlock(text_prop=TextProp("test10")),
        NotionTextBlock(text_prop=TextProp("test11")),
        NotionTextBlock(text_prop=TextProp("test12")),
        NotionTextBlock(text_prop=TextProp("test13")),
    ]


def test_paragraphs(parse_html):
    test_note = parse_html(
        "<address>test1</address>"
        "<pre>test2</pre>"
        "<p>test3</p>"
        "<blockquote>test4</blockquote>"
        "<dl>test5</dl>"
        "<dt>test6</dt>"
    )

    assert parse_webclip(test_note) == [
        NotionTextBlock(text_prop=TextProp("test1")),
        NotionTextBlock(text_prop=TextProp("test2")),
        NotionTextBlock(text_prop=TextProp("test3")),
        NotionTextBlock(text_prop=TextProp("test4")),
        NotionTextBlock(text_prop=TextProp("test5")),
        NotionTextBlock(text_prop=TextProp("test6")),
    ]


def test_subheaders(parse_html):
    test_note = parse_html("<h4>test1</h4><h5>test2</h5><h5>test3</h5>")

    assert parse_webclip(test_note) == [
        NotionSubsubheaderBlock(text_prop=TextProp("test1")),
        NotionSubsubheaderBlock(text_prop=TextProp("test2")),
        NotionSubsubheaderBlock(text_prop=TextProp("test3")),
    ]


def test_inline_modifiers(parse_html):
    test_note = parse_html(
        "<strong>strong</strong>"
        "<em>em</em>"
        "<cite>cite</cite>"
        "<dfn>dfn</dfn>"
        "<abbr>abbr</abbr>"
        "<acronym>acronym</acronym>"
        "<strike>strike</strike>"
        "<del>del</del>"
    )

    assert parse_webclip(test_note) == [
        NotionTextBlock(text_prop=TextProp("strong", properties=[["strong", [["b"]]]])),
        NotionTextBlock(text_prop=TextProp("em", properties=[["em", [["i"]]]])),
        NotionTextBlock(text_prop=TextProp("cite", properties=[["cite", [["i"]]]])),
        NotionTextBlock(text_prop=TextProp("dfn", properties=[["dfn", [["i"]]]])),
        NotionTextBlock(text_prop=TextProp("abbr", properties=[["abbr", [["i"]]]])),
        NotionTextBlock(
            text_prop=TextProp("acronym", properties=[["acronym", [["i"]]]])
        ),
        NotionTextBlock(text_prop=TextProp("strike", properties=[["strike", [["s"]]]])),
        NotionTextBlock(text_prop=TextProp("del", properties=[["del", [["s"]]]])),
    ]


def test_textless_links(parse_html):
    test_note = parse_html(
        '<a href="http://google1.com"></a><a href="http://google2.com">     </a>'
    )

    assert parse_webclip(test_note) == [
        NotionTextBlock(
            text_prop=TextProp(
                "http://google1.com",
                properties=[["http://google1.com", [["a", "http://google1.com"]]]],
            )
        ),
        NotionTextBlock(
            text_prop=TextProp(
                "http://google2.com",
                properties=[["http://google2.com", [["a", "http://google2.com"]]]],
            )
        ),
    ]


def test_newlines(parse_html):
    test_note = parse_html("<div>test1<br>test2</div>")

    assert parse_webclip(test_note) == [
        NotionTextBlock(text_prop=TextProp("test1\ntest2"))
    ]


def test_remove_empty(parse_html):
    test_note = parse_html("<div></div>")

    assert parse_webclip(test_note) == []


def test_strip_paragraphs(parse_html):
    test_note = parse_html(
        "<ul><li><div><br /></div></li></ul>"
        "<div>  test1  </div>"
        "<div>  <span>test2</span>  </div>"
        "<ul><li><div></div></li></ul>"
    )

    assert parse_webclip(test_note) == [
        NotionBulletedListBlock(text_prop=TextProp("")),
        NotionTextBlock(text_prop=TextProp("test1")),
        NotionTextBlock(text_prop=TextProp("test2")),
        NotionBulletedListBlock(text_prop=TextProp("")),
    ]


def test_flatten_split_block(parse_html):
    test_note = parse_html("<div>test1<div>test2</div>test3</div>")

    assert parse_webclip(test_note) == [
        NotionTextBlock(text_prop=TextProp("test1")),
        NotionTextBlock(text_prop=TextProp("test2")),
        NotionTextBlock(text_prop=TextProp("test3")),
    ]


def test_flatten_extract_embed(parse_html):
    test_note = parse_html("<div><div>test1</div></div>")

    assert parse_webclip(test_note) == [
        NotionTextBlock(text_prop=TextProp("test1")),
    ]


def test_flatten_string(parse_html):
    test_note = parse_html("test")

    assert parse_webclip(test_note) == [
        NotionTextBlock(text_prop=TextProp("test")),
    ]


def test_flatten_bad_inline(parse_html):
    test_note = parse_html("<div><span><div>test</div></span></div>")

    assert parse_webclip(test_note) == [
        NotionTextBlock(text_prop=TextProp("test")),
    ]


def test_embedded_inline_img_bin_bad_quotes(parse_html, smallest_gif):
    test_note = parse_html(
        f"<img src=\"'data:{smallest_gif.mime};"
        f'base64,{base64.b64encode(smallest_gif.data_bin).decode("utf-8")}\'" />'
    )

    result_block = parse_webclip(test_note)[0]

    assert result_block == NotionImageBlock(
        md5_hash=smallest_gif.md5,
        resource=EvernoteResource(
            data_bin=smallest_gif.data_bin,
            size=smallest_gif.size,
            md5=smallest_gif.md5,
            mime=smallest_gif.mime,
            file_name=f"{smallest_gif.md5}.gif",
        ),
    )
