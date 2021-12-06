import datetime
import logging
from pathlib import Path

import pytest
from dateutil.tz import tzutc

from enex2notion.enex_parser import EvernoteNote, EvernoteResource, iter_notes


def test_iter_notes_single(fs):
    test_enex = """<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export4.dtd">
    <en-export export-date="20211218T085932Z" application="Evernote" version="10.25.6">
      <note>
        <title>test1</title>
        <created>20211118T085332Z</created>
        <updated>20211118T085920Z</updated>
        <note-attributes>
        </note-attributes>
        <content>test</content>
      </note>
    </en-export>
    """
    fs.create_file("test.enex", contents=test_enex)

    notes = list(iter_notes(Path("test.enex")))

    assert notes == [
        EvernoteNote(
            title="test1",
            created=datetime.datetime(2021, 11, 18, 8, 53, 32, tzinfo=tzutc()),
            updated=datetime.datetime(2021, 11, 18, 8, 59, 20, tzinfo=tzutc()),
            content="test",
            tags=[],
            author="",
            url="",
            is_webclip=False,
            resources=[],
        ),
    ]


def test_iter_notes_single_hash(fs):
    test_enex = """<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export4.dtd">
    <en-export export-date="20211218T085932Z" application="Evernote" version="10.25.6">
      <note>
        <title>test1</title>
        <created>20211118T085332Z</created>
        <updated>20211118T085920Z</updated>
        <note-attributes>
        </note-attributes>
        <content>test</content>
      </note>
    </en-export>
    """
    fs.create_file("test.enex", contents=test_enex)

    notes = list(iter_notes(Path("test.enex")))

    assert notes[0].note_hash == "2f0e42350f1954c46ff8015d9ca81458f9477fca"


def test_iter_notes_single_tags(fs):
    test_enex = """<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export4.dtd">
    <en-export export-date="20211218T085932Z" application="Evernote" version="10.25.6">
      <note>
        <title>test1</title>
        <created>20211118T085332Z</created>
        <updated>20211118T085920Z</updated>
        <tag>tag1</tag>
        <tag>tag2</tag>
        <note-attributes>
        </note-attributes>
        <content>test</content>
      </note>
    </en-export>
    """
    fs.create_file("test.enex", contents=test_enex)

    notes = list(iter_notes(Path("test.enex")))

    assert notes == [
        EvernoteNote(
            title="test1",
            created=datetime.datetime(2021, 11, 18, 8, 53, 32, tzinfo=tzutc()),
            updated=datetime.datetime(2021, 11, 18, 8, 59, 20, tzinfo=tzutc()),
            content="test",
            tags=["tag1", "tag2"],
            author="",
            url="",
            is_webclip=False,
            resources=[],
        ),
    ]


def test_iter_notes_single_one_tag(fs):
    test_enex = """<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export4.dtd">
    <en-export export-date="20211218T085932Z" application="Evernote" version="10.25.6">
      <note>
        <title>test1</title>
        <created>20211118T085332Z</created>
        <updated>20211118T085920Z</updated>
        <tag>tag1</tag>
        <note-attributes>
        </note-attributes>
        <content>test</content>
      </note>
    </en-export>
    """
    fs.create_file("test.enex", contents=test_enex)

    notes = list(iter_notes(Path("test.enex")))

    assert notes == [
        EvernoteNote(
            title="test1",
            created=datetime.datetime(2021, 11, 18, 8, 53, 32, tzinfo=tzutc()),
            updated=datetime.datetime(2021, 11, 18, 8, 59, 20, tzinfo=tzutc()),
            content="test",
            tags=["tag1"],
            author="",
            url="",
            is_webclip=False,
            resources=[],
        ),
    ]


def test_iter_notes_single_attrs(fs):
    test_enex = """<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export4.dtd">
    <en-export export-date="20211218T085932Z" application="Evernote" version="10.25.6">
      <note>
        <title>test1</title>
        <created>20211118T085332Z</created>
        <updated>20211118T085920Z</updated>
        <note-attributes>
            <author>test@user.com</author>
            <source-url>https://google.com</source-url>
        </note-attributes>
        <content>test</content>
      </note>
    </en-export>
    """
    fs.create_file("test.enex", contents=test_enex)

    notes = list(iter_notes(Path("test.enex")))

    assert notes == [
        EvernoteNote(
            title="test1",
            created=datetime.datetime(2021, 11, 18, 8, 53, 32, tzinfo=tzutc()),
            updated=datetime.datetime(2021, 11, 18, 8, 59, 20, tzinfo=tzutc()),
            content="test",
            tags=[],
            author="test@user.com",
            url="https://google.com",
            is_webclip=False,
            resources=[],
        ),
    ]


def test_iter_notes_webclip1(fs):
    test_enex = """<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export4.dtd">
    <en-export export-date="20211218T085932Z" application="Evernote" version="10.25.6">
      <note>
        <title>test1</title>
        <created>20211118T085332Z</created>
        <updated>20211118T085920Z</updated>
        <note-attributes>
            <source>web.clip</source>
        </note-attributes>
        <content>test</content>
      </note>
    </en-export>
    """
    fs.create_file("test.enex", contents=test_enex)

    notes = list(iter_notes(Path("test.enex")))

    assert notes == [
        EvernoteNote(
            title="test1",
            created=datetime.datetime(2021, 11, 18, 8, 53, 32, tzinfo=tzutc()),
            updated=datetime.datetime(2021, 11, 18, 8, 59, 20, tzinfo=tzutc()),
            content="test",
            tags=[],
            author="",
            url="",
            is_webclip=True,
            resources=[],
        ),
    ]


def test_iter_notes_webclip2(fs):
    test_enex = """<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export4.dtd">
    <en-export export-date="20211218T085932Z" application="Evernote" version="10.25.6">
      <note>
        <title>test1</title>
        <created>20211118T085332Z</created>
        <updated>20211118T085920Z</updated>
        <note-attributes>
            <source-application>webclipper.evernote</source-application>
        </note-attributes>
        <content>test</content>
      </note>
    </en-export>
    """
    fs.create_file("test.enex", contents=test_enex)

    notes = list(iter_notes(Path("test.enex")))

    assert notes == [
        EvernoteNote(
            title="test1",
            created=datetime.datetime(2021, 11, 18, 8, 53, 32, tzinfo=tzutc()),
            updated=datetime.datetime(2021, 11, 18, 8, 59, 20, tzinfo=tzutc()),
            content="test",
            tags=[],
            author="",
            url="",
            is_webclip=True,
            resources=[],
        ),
    ]


def test_iter_notes_webclip_content(fs):
    test_enex = """<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export4.dtd">
    <en-export export-date="20211218T085932Z" application="Evernote" version="10.25.6">
      <note>
        <title>test1</title>
        <created>20211118T085332Z</created>
        <updated>20211118T085920Z</updated>
        <note-attributes>
        </note-attributes>
        <content><![CDATA[
        <div style="--en-clipped-content:article;">test</div>
        ]]></content>
      </note>
    </en-export>
    """
    fs.create_file("test.enex", contents=test_enex)

    notes = list(iter_notes(Path("test.enex")))

    assert notes == [
        EvernoteNote(
            title="test1",
            created=datetime.datetime(2021, 11, 18, 8, 53, 32, tzinfo=tzutc()),
            updated=datetime.datetime(2021, 11, 18, 8, 59, 20, tzinfo=tzutc()),
            content='<div style="--en-clipped-content:article;">test</div>',
            tags=[],
            author="",
            url="",
            is_webclip=True,
            resources=[],
        ),
    ]


def test_iter_notes_multi(fs):
    test_enex = """<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export4.dtd">
    <en-export export-date="20211218T085932Z" application="Evernote" version="10.25.6">
      <note>
        <title>test1</title>
        <created>20211118T085332Z</created>
        <updated>20211118T085920Z</updated>
        <note-attributes>
        </note-attributes>
        <content>test</content>
      </note>
      <note>
        <title>test2</title>
        <created>20211119T085332Z</created>
        <updated>20211119T085920Z</updated>
        <note-attributes>
        </note-attributes>
        <content>test</content>
      </note>
    </en-export>
    """
    fs.create_file("test.enex", contents=test_enex)

    notes = list(iter_notes(Path("test.enex")))

    assert notes == [
        EvernoteNote(
            title="test1",
            created=datetime.datetime(2021, 11, 18, 8, 53, 32, tzinfo=tzutc()),
            updated=datetime.datetime(2021, 11, 18, 8, 59, 20, tzinfo=tzutc()),
            content="test",
            tags=[],
            author="",
            url="",
            is_webclip=False,
            resources=[],
        ),
        EvernoteNote(
            title="test2",
            created=datetime.datetime(2021, 11, 19, 8, 53, 32, tzinfo=tzutc()),
            updated=datetime.datetime(2021, 11, 19, 8, 59, 20, tzinfo=tzutc()),
            content="test",
            tags=[],
            author="",
            url="",
            is_webclip=False,
            resources=[],
        ),
    ]


def test_iter_notes_single_with_resource(fs):
    test_enex = """<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export4.dtd">
    <en-export export-date="20211218T085932Z" application="Evernote" version="10.25.6">
      <note>
        <title>test1</title>
        <created>20211118T085332Z</created>
        <updated>20211118T085920Z</updated>
        <note-attributes>
        </note-attributes>
        <content>test</content>
        <resource>
          <data encoding="base64">
            R0lGODlhAQABAAAAACwAAAAAAQABAAAC
          </data>
          <mime>image/gif</mime>
          <resource-attributes>
            <file-name>smallest.gif</file-name>
          </resource-attributes>
        </resource>
      </note>
    </en-export>
    """
    fs.create_file("test.enex", contents=test_enex)

    notes = list(iter_notes(Path("test.enex")))

    expected_resource = EvernoteResource(
        data_bin=(
            b"GIF89a\x01\x00\x01\x00\x00\x00\x00,"
            b"\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
        ),
        size=24,
        md5="bc32ed98d624acb4008f986349a20d26",
        mime="image/gif",
        file_name="smallest.gif",
    )

    assert notes == [
        EvernoteNote(
            title="test1",
            created=datetime.datetime(2021, 11, 18, 8, 53, 32, tzinfo=tzutc()),
            updated=datetime.datetime(2021, 11, 18, 8, 59, 20, tzinfo=tzutc()),
            content="test",
            tags=[],
            author="",
            url="",
            is_webclip=False,
            resources=[expected_resource],
        ),
    ]
    assert (
        notes[0].resource_by_md5("bc32ed98d624acb4008f986349a20d26")
        == expected_resource
    )
    assert notes[0].resource_by_md5("000") is None


def test_iter_notes_single_with_noname_resource(fs, mocker):
    test_enex = """<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export4.dtd">
    <en-export export-date="20211218T085932Z" application="Evernote" version="10.25.6">
      <note>
        <title>test1</title>
        <created>20211118T085332Z</created>
        <updated>20211118T085920Z</updated>
        <note-attributes>
        </note-attributes>
        <content>test</content>
        <resource>
          <data encoding="base64">
            R0lGODlhAQABAAAAACwAAAAAAQABAAAC
          </data>
          <mime>image/gif</mime>
          <resource-attributes>
          </resource-attributes>
        </resource>
      </note>
    </en-export>
    """
    fs.create_file("test.enex", contents=test_enex)

    mocker.patch("enex2notion.enex_parser.uuid.uuid4", return_value="test-uuid")

    notes = list(iter_notes(Path("test.enex")))

    assert notes == [
        EvernoteNote(
            title="test1",
            created=datetime.datetime(2021, 11, 18, 8, 53, 32, tzinfo=tzutc()),
            updated=datetime.datetime(2021, 11, 18, 8, 59, 20, tzinfo=tzutc()),
            content="test",
            tags=[],
            author="",
            url="",
            is_webclip=False,
            resources=[
                EvernoteResource(
                    data_bin=(
                        b"GIF89a\x01\x00\x01\x00\x00\x00\x00,"
                        b"\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02"
                    ),
                    size=24,
                    md5="bc32ed98d624acb4008f986349a20d26",
                    mime="image/gif",
                    file_name="test-uuid.gif",
                )
            ],
        ),
    ]


def test_iter_notes_single_with_empty_resource(fs, caplog):
    test_enex = """<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export4.dtd">
    <en-export export-date="20211218T085932Z" application="Evernote" version="10.25.6">
      <note>
        <title>test1</title>
        <created>20211118T085332Z</created>
        <updated>20211118T085920Z</updated>
        <note-attributes>
        </note-attributes>
        <content>test</content>
        <resource>
          <data encoding="base64">
          </data>
          <mime>image/gif</mime>
          <resource-attributes>
            <file-name>smallest.gif</file-name>
          </resource-attributes>
        </resource>
      </note>
    </en-export>
    """
    fs.create_file("test.enex", contents=test_enex)

    with caplog.at_level(logging.WARNING):
        notes = list(iter_notes(Path("test.enex")))

    expected_resource = EvernoteResource(
        data_bin=b"",
        size=0,
        md5="d41d8cd98f00b204e9800998ecf8427e",
        mime="image/gif",
        file_name="smallest.gif",
    )

    assert "Empty resource" in caplog.records[0].message
    assert notes == [
        EvernoteNote(
            title="test1",
            created=datetime.datetime(2021, 11, 18, 8, 53, 32, tzinfo=tzutc()),
            updated=datetime.datetime(2021, 11, 18, 8, 59, 20, tzinfo=tzutc()),
            content="test",
            tags=[],
            author="",
            url="",
            is_webclip=False,
            resources=[expected_resource],
        ),
    ]
    assert (
        notes[0].resource_by_md5("d41d8cd98f00b204e9800998ecf8427e")
        == expected_resource
    )
