from enex2notion.notion_blocks import TextProp
from enex2notion.string_extractor import extract_string


def test_extract_text(parse_html):
    test_note = parse_html("<div>test1</div>")

    assert extract_string(test_note) == TextProp(text="test1", properties=[["test1"]])


def test_extract_text_inside(parse_html):
    test_note = parse_html("test1")

    assert extract_string(test_note) == TextProp(text="test1", properties=[["test1"]])


def test_extract_text_newline(parse_html):
    test_note = parse_html("<div>test1</div><div>test2</div>")

    assert extract_string(test_note) == TextProp(
        text="test1\ntest2", properties=[["test1\ntest2"]]
    )


def test_extract_text_newline_inline(parse_html):
    test_note = parse_html("<div>test1<br />test2</div>")

    assert extract_string(test_note) == TextProp(
        text="test1\ntest2", properties=[["test1\ntest2"]]
    )


def test_extract_text_overlap(parse_html):
    test_note = parse_html(
        "<div>head <b>middle_head <i>inside</i> middle_tail</b> tail</div>"
    )

    assert extract_string(test_note) == TextProp(
        text="head middle_head inside middle_tail tail",
        properties=[
            ["head "],
            ["middle_head ", [["b"]]],
            ["inside", [["b"], ["i"]]],
            [" middle_tail", [["b"]]],
            [" tail"],
        ],
    )


def test_extract_text_style_bold(parse_html):
    test_note = parse_html('<div><span style="font-weight: bold;">bold</span></div>')

    assert extract_string(test_note) == TextProp(
        text="bold",
        properties=[["bold", [["b"]]]],
    )


def test_extract_text_style_italic(parse_html):
    test_note = parse_html('<div><span style="font-style: italic;">italic</span></div>')

    assert extract_string(test_note) == TextProp(
        text="italic",
        properties=[["italic", [["i"]]]],
    )


def test_extract_text_style_bold_italic(parse_html):
    test_note = parse_html(
        "<div>"
        '<span style="font-weight: bold; font-style: italic;">bold italic</span>'
        "</div>"
    )

    assert extract_string(test_note) == TextProp(
        text="bold italic",
        properties=[["bold italic", [["b"], ["i"]]]],
    )


def test_extract_text_bold(parse_html):
    test_note = parse_html("<div><b>test1</b></div>")

    assert extract_string(test_note) == TextProp(
        text="test1", properties=[["test1", [["b"]]]]
    )


def test_extract_text_italic(parse_html):
    test_note = parse_html("<div><i>test1</i></div>")

    assert extract_string(test_note) == TextProp(
        text="test1", properties=[["test1", [["i"]]]]
    )


def test_extract_text_strikethrough(parse_html):
    test_note = parse_html("<div><s>test1</s></div>")

    assert extract_string(test_note) == TextProp(
        text="test1", properties=[["test1", [["s"]]]]
    )


def test_extract_text_underline(parse_html):
    test_note = parse_html("<div><u>test1</u></div>")

    assert extract_string(test_note) == TextProp(
        text="test1", properties=[["test1", [["_"]]]]
    )


def test_extract_text_url(parse_html):
    test_note = parse_html('<div><a href="https://google.com">test1</a></div>')

    assert extract_string(test_note) == TextProp(
        text="test1", properties=[["test1", [["a", "https://google.com"]]]]
    )


def test_extract_text_url_empty(parse_html):
    test_note = parse_html("<div><a>test1</a></div>")

    assert extract_string(test_note) == TextProp(text="test1", properties=[["test1"]])


def test_extract_span_empty(parse_html):
    test_note = parse_html("<div><span>empty</span></div>")

    assert extract_string(test_note) == TextProp(text="empty", properties=[["empty"]])


def test_extract_text_color(parse_html):
    test_note = parse_html(
        '<div><span style="color:rgb(90, 90, 90);">dark gray</span></div>'
        '<div><span style="color:rgb(140, 140, 140);">gray</span></div>'
        '<div><span style="color:rgb(191, 191, 191);">light gray</span></div>'
        '<div><span style="color:rgb(87, 36, 194);">dark purple</span></div>'
        '<div><span style="color:rgb(182, 41, 212);">purple</span></div>'
        '<div><span style="color:rgb(252, 18, 51);">red</span></div>'
        '<div><span style="color:rgb(251, 95, 44);">orange</span></div>'
        '<div><span style="color:rgb(229, 158, 37);">yellow</span></div>'
        '<div><span style="color:rgb(24, 168, 65);">green</span></div>'
        '<div><span style="color:rgb(26, 169, 178);">teal</span></div>'
        '<div><span style="color:rgb(24, 133, 226);">blue</span></div>'
        '<div><span style="color:rgb(13, 58, 153);">navy</span></div>'
    )

    assert extract_string(test_note) == TextProp(
        text=(
            "dark gray\n"
            "gray\n"
            "light gray\n"
            "dark purple\n"
            "purple\n"
            "red\n"
            "orange\n"
            "yellow\n"
            "green\n"
            "teal\n"
            "blue\n"
            "navy"
        ),
        properties=[
            ["dark gray", [["h", "gray"]]],
            ["\n"],
            ["gray", [["h", "gray"]]],
            ["\n"],
            ["light gray", [["h", "gray"]]],
            ["\n"],
            ["dark purple", [["h", "purple"]]],
            ["\n"],
            ["purple", [["h", "purple"]]],
            ["\n"],
            ["red", [["h", "red"]]],
            ["\n"],
            ["orange", [["h", "orange"]]],
            ["\n"],
            ["yellow", [["h", "yellow"]]],
            ["\n"],
            ["green", [["h", "teal"]]],
            ["\n"],
            ["teal", [["h", "blue"]]],
            ["\n"],
            ["blue", [["h", "blue"]]],
            ["\n"],
            ["navy", [["h", "blue"]]],
        ],
    )


def test_extract_text_color_black(parse_html):
    test_note = parse_html(
        '<div><span style="color:rgb(51, 51, 51);">black</span></div>'
        '<div><span style="color:rgb(255, 255, 255);">white</span></div>'
        '<div><span style="background-color:rgb(51, 51, 51);">black</span></div>'
        '<div><span style="background-color:rgb(255, 255, 255);">white</span></div>'
    )

    assert extract_string(test_note) == TextProp(
        text="black\nwhite\nblack\nwhite",
        properties=[["black\nwhite\nblack\nwhite"]],
    )


def test_extract_text_color_strange(parse_html):
    test_note = parse_html(
        '<div><span style="color:magentific;">strange</span></div>'
        '<div><span style="background-color:magentific;">strange</span></div>'
    )

    assert extract_string(test_note) == TextProp(
        text="strange\nstrange",
        properties=[["strange\nstrange"]],
    )


def test_extract_text_color_empty(parse_html):
    test_note = parse_html('<div><span style="color:;--boop">empty</span></div>')

    assert extract_string(test_note) == TextProp(
        text="empty",
        properties=[["empty"]],
    )


def test_extract_text_bad_css(parse_html):
    test_note = parse_html('<div><span style="--boop">bad</span></div>')

    assert extract_string(test_note) == TextProp(text="bad", properties=[["bad"]])


def test_extract_text_color_near(parse_html):
    test_note = parse_html(
        '<div><span style="color:rgb(200, 158, 37);">yellow</span></div>'
        '<div><span style="background-color: rgb(200, 158, 37);">yellow</span></div>'
    )

    assert extract_string(test_note) == TextProp(
        text="yellow\nyellow",
        properties=[
            ["yellow", [["h", "yellow"]]],
            ["\n"],
            ["yellow", [["h", "yellow_background"]]],
        ],
    )


def test_extract_text_color_background(parse_html):
    test_note = parse_html(
        '<div><span style="background-color: rgb(255, 250, 165);">yellow old</span>'
        "</div>"
        '<div><span style="background-color: #ffef9e;">yellow</span></div>'
        '<div><span style="background-color: #fec1d0;">red</span></div>'
        '<div><span style="background-color: #b7f7d1;">green</span></div>'
        '<div><span style="background-color: #adecf4;">blue</span></div>'
        '<div><span style="background-color: #cbcaff;">purple</span></div>'
        '<div><span style="background-color: #ffd1b0;">orange</span></div>'
    )

    assert extract_string(test_note) == TextProp(
        text="yellow old\nyellow\nred\ngreen\nblue\npurple\norange",
        properties=[
            ["yellow old", [["h", "yellow_background"]]],
            ["\n"],
            ["yellow", [["h", "yellow_background"]]],
            ["\n"],
            ["red", [["h", "red_background"]]],
            ["\n"],
            ["green", [["h", "teal_background"]]],
            ["\n"],
            ["blue", [["h", "blue_background"]]],
            ["\n"],
            ["purple", [["h", "purple_background"]]],
            ["\n"],
            ["orange", [["h", "orange_background"]]],
        ],
    )


def test_extract_text_color_background_highlight(parse_html):
    test_note = parse_html(
        '<div><span style="--en-highlight:yellow;">yellow</span></div>'
        '<div><span style="--en-highlight:red;">red</span></div>'
        '<div><span style="--en-highlight:green;">green</span></div>'
        '<div><span style="--en-highlight:blue;">blue</span></div>'
        '<div><span style="--en-highlight:purple;">purple</span></div>'
        '<div><span style="--en-highlight:orange;">orange</span></div>'
    )

    assert extract_string(test_note) == TextProp(
        text="yellow\nred\ngreen\nblue\npurple\norange",
        properties=[
            ["yellow", [["h", "yellow_background"]]],
            ["\n"],
            ["red", [["h", "red_background"]]],
            ["\n"],
            ["green", [["h", "teal_background"]]],
            ["\n"],
            ["blue", [["h", "blue_background"]]],
            ["\n"],
            ["purple", [["h", "purple_background"]]],
            ["\n"],
            ["orange", [["h", "orange_background"]]],
        ],
    )


def test_extract_text_color_background_highlight_unknown(parse_html):
    test_note = parse_html(
        '<div><span style="--en-highlight:glurpurle;">glurpurle</span></div>'
    )

    assert extract_string(test_note) == TextProp(
        text="glurpurle", properties=[["glurpurle"]]
    )


def test_extract_text_color_inversion(parse_html):
    test_note = parse_html(
        "<div>"
        '<span style="color:rgb(229, 158, 37);--inversion-type-color:simple;">'
        "yellow"
        "</span>"
        "</div>"
    )

    assert extract_string(test_note) == TextProp(
        text="yellow", properties=[["yellow", [["h", "yellow"]]]]
    )
