from datetime import datetime

import pytest
from dateutil.tz import tzutc

from enex2notion.enex_types import EvernoteNote, EvernoteResource
from enex2notion.note_parser import parse_note
from enex2notion.notion_blocks_uploadable import NotionPDFBlock


@pytest.fixture()
def mock_pdf_block():
    zero_md5 = "d41d8cd98f00b204e9800998ecf8427e"

    return NotionPDFBlock(
        md5_hash=zero_md5,
        resource=EvernoteResource(
            data_bin=b"",
            size=0,
            md5=zero_md5,
            mime="application/pdf",
            file_name=f"{zero_md5}.pdf",
        ),
    )


@pytest.fixture()
def mock_pdfkit(mocker):
    mock_pdfkit = mocker.patch("enex2notion.note_parser_webclip_pdf.pdfkit.from_string")
    mock_pdfkit.return_value = b""

    return mock_pdfkit


def test_simple(mock_pdfkit, mock_pdf_block):
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

    result_blocks = parse_note(test_note, mode_webclips="PDF")
    result_html = mock_pdfkit.call_args[0][0]

    assert result_html == test_note.content
    assert result_blocks == [mock_pdf_block]


def test_local_image(mock_pdfkit, mock_pdf_block, smallest_gif):
    test_note = EvernoteNote(
        title="test1",
        created=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        updated=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        content=(
            f'<en-note><en-media type="{smallest_gif.mime}"'
            f' width="100" height="100" hash="{smallest_gif.md5}"></en-note>'
        ),
        tags=[],
        author="",
        url="",
        is_webclip=True,
        resources=[smallest_gif],
    )

    expected_html = (
        '<en-note><img height="100"'
        ' src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEAAAAALAAAAAABAAEAAAIA"'
        ' width="100"></img></en-note>'
    )

    result_blocks = parse_note(test_note, mode_webclips="PDF")
    result_html = mock_pdfkit.call_args[0][0]

    assert result_html == expected_html
    assert result_blocks == [mock_pdf_block]


def test_local_image_bad(mock_pdfkit, mock_pdf_block):
    test_note = EvernoteNote(
        title="test1",
        created=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        updated=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        content='<en-note><en-media type="fake/mime" hash="fake_md5"></en-note>',
        tags=[],
        author="",
        url="",
        is_webclip=True,
        resources=[],
    )

    expected_html = "<en-note></en-note>"

    result_blocks = parse_note(test_note, mode_webclips="PDF")
    result_html = mock_pdfkit.call_args[0][0]

    assert result_html == expected_html
    assert result_blocks == [mock_pdf_block]


def test_remote_images(mock_pdfkit, mock_pdf_block):
    test_note = EvernoteNote(
        title="test1",
        created=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        updated=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        content='<en-note><img src="http://google.com"/></en-note>',
        tags=[],
        author="",
        url="",
        is_webclip=True,
        resources=[],
    )

    expected_html = "<en-note></en-note>"

    result_blocks = parse_note(test_note, mode_webclips="PDF")
    result_html = mock_pdfkit.call_args[0][0]

    assert result_html == expected_html
    assert result_blocks == [mock_pdf_block]


def test_remote_images_css(mock_pdfkit, mock_pdf_block):
    test_note = EvernoteNote(
        title="test1",
        created=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        updated=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        content=(
            "<en-note>"
            '<div style="background-image: url(http://google.com)"/></div>'
            "</en-note>"
        ),
        tags=[],
        author="",
        url="",
        is_webclip=True,
        resources=[],
    )

    expected_html = '<en-note><div style="background-image: "></div></en-note>'

    result_blocks = parse_note(test_note, mode_webclips="PDF")
    result_html = mock_pdfkit.call_args[0][0]

    assert result_html == expected_html
    assert result_blocks == [mock_pdf_block]


def test_data_images(mock_pdfkit, mock_pdf_block):
    test_note = EvernoteNote(
        title="test1",
        created=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        updated=datetime(2021, 11, 18, 0, 0, 0, tzinfo=tzutc()),
        content='<en-note><img src="data:image/gif;base64,IA=="></img></en-note>',
        tags=[],
        author="",
        url="",
        is_webclip=True,
        resources=[],
    )

    expected_html = '<en-note><img src="data:image/gif;base64,IA=="/></en-note>'

    result_blocks = parse_note(test_note, mode_webclips="PDF")
    result_html = mock_pdfkit.call_args[0][0]

    assert result_html == expected_html
    assert result_blocks == [mock_pdf_block]
