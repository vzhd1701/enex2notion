import logging

import pytest

from enex2notion.cli import cli


@pytest.fixture()
def mock_api(mocker):
    return {
        "NotionClient": mocker.patch("enex2notion.cli.NotionClient"),
        "get_import_root": mocker.patch("enex2notion.cli.get_import_root"),
        "get_notebook_database": mocker.patch("enex2notion.cli.get_notebook_database"),
        "get_notebook_page": mocker.patch("enex2notion.cli.get_notebook_page"),
        "upload_note": mocker.patch("enex2notion.cli.upload_note"),
        "parse_note": mocker.patch("enex2notion.cli.parse_note"),
    }


@pytest.fixture()
def fake_note_factory(mocker):
    mock_iter = mocker.patch("enex2notion.cli.iter_notes")
    mock_iter.return_value = [mocker.MagicMock(note_hash="fake_hash", is_webclip=False)]

    return mock_iter


def test_dry_run(mock_api, fake_note_factory):
    cli(["fake.enex"])

    mock_api["get_import_root"].assert_not_called()


def test_dir(mock_api, fake_note_factory, fs):
    fs.makedir("test_dir")
    fs.create_file("test_dir/test.enex")

    cli(["test_dir"])

    mock_api["parse_note"].assert_called_once()


def test_empty_dir(mock_api, fake_note_factory, fs):
    fs.makedir("test_dir")

    cli(["test_dir"])

    mock_api["upload_note"].assert_not_called()


def test_verbose(mock_api, fake_note_factory, mocker):
    fake_logs = {}
    mock_logger = mocker.patch("enex2notion.cli.logging")
    mock_logger.getLogger = lambda name: fake_logs.setdefault(name, mocker.MagicMock())

    cli(["--verbose", "fake.enex"])

    mock_logger.basicConfig.assert_called_once_with(format=mocker.ANY)
    mock_logger.getLogger("enex2notion").setLevel.assert_called_with(mock_logger.DEBUG)


def test_no_verbose(mock_api, fake_note_factory, mocker):
    fake_logs = {}
    mock_logger = mocker.patch("enex2notion.cli.logging")
    mock_logger.getLogger = lambda name: fake_logs.setdefault(name, mocker.MagicMock())

    cli(["fake.enex"])

    mock_logger.basicConfig.assert_called_once_with(format=mocker.ANY)
    mock_logger.getLogger("enex2notion").setLevel.assert_called_with(mock_logger.INFO)


def test_db_mode(mock_api, fake_note_factory, mocker):
    cli(["--token", "fake_token", "fake.enex"])

    mock_api["get_notebook_page"].assert_not_called()
    mock_api["get_notebook_database"].assert_called_once_with(mocker.ANY, "fake")


def test_page_mode(mock_api, fake_note_factory, mocker):
    cli(["--token", "fake_token", "--mode", "PAGE", "fake.enex"])

    mock_api["get_notebook_database"].assert_not_called()
    mock_api["get_notebook_page"].assert_called_once_with(mocker.ANY, "fake")


def test_add_meta(mock_api, fake_note_factory, mocker):
    cli(["--add-meta", "fake.enex"])

    mock_api["parse_note"].assert_called_once_with(
        mocker.ANY, mode_webclips="TXT", is_add_meta=True
    )


def test_skip_dupe(mock_api, fake_note_factory, mocker):
    cli(["--token", "fake_token", "fake.enex"])

    fake_note_factory.return_value = [
        mocker.MagicMock(note_hash="fake_hash"),
        mocker.MagicMock(note_hash="fake_hash"),
    ]

    mock_api["upload_note"].assert_called_once()


def test_done_file(mock_api, fake_note_factory, mocker, fs):
    fs.create_file("done.txt")

    fake_note_factory.return_value = [
        mocker.MagicMock(note_hash="fake_hash1", is_webclip=False),
        mocker.MagicMock(note_hash="fake_hash2", is_webclip=False),
    ]

    cli(["--token", "fake_token", "--done-file", "done.txt", "fake.enex"])

    with open("done.txt") as f:
        done_result = f.read()

    assert mock_api["upload_note"].call_count == 2
    assert done_result == "fake_hash1\nfake_hash2\n"


def test_done_file_populated(mock_api, fake_note_factory, mocker, fs):
    fs.create_file("done.txt", contents="fake_hash1\nfake_hash2\n")

    fake_note_factory.return_value = [
        mocker.MagicMock(note_hash="fake_hash1"),
        mocker.MagicMock(note_hash="fake_hash2"),
    ]

    cli(["--token", "fake_token", "--done-file", "done.txt", "fake.enex"])

    mock_api["upload_note"].assert_not_called()


def test_done_file_empty(mock_api, fake_note_factory, fs):
    fake_note_factory.return_value = []

    cli(["--token", "fake_token", "--done-file", "done.txt", "fake.enex"])

    mock_api["upload_note"].assert_not_called()


def test_bad_file(mock_api, fake_note_factory):
    mock_api["parse_note"].return_value = []

    cli(["fake.enex"])

    mock_api["parse_note"].assert_called_once()


def test_webclip(mock_api, fake_note_factory, mocker):
    fake_note_factory.return_value = [
        mocker.MagicMock(note_hash="fake_hash1", is_webclip=True),
    ]

    cli(["fake.enex"])

    mock_api["parse_note"].assert_called_once_with(
        mocker.ANY, mode_webclips="TXT", is_add_meta=False
    )


def test_webclip_pdf(mock_api, fake_note_factory, mocker):
    fake_note_factory.return_value = [
        mocker.MagicMock(note_hash="fake_hash1", is_webclip=True),
    ]

    mocker.patch("enex2notion.cli.ensure_wkhtmltopdf")

    cli(["--mode-webclips", "PDF", "fake.enex"])

    mock_api["parse_note"].assert_called_once_with(
        mocker.ANY, mode_webclips="PDF", is_add_meta=False
    )


def test_unhandled_exception(mock_api, fake_note_factory, caplog):
    fake_exception = Exception("fake")
    mock_api["parse_note"].side_effect = fake_exception

    with caplog.at_level(logging.ERROR, logger="enex2notion"):
        with pytest.raises(Exception) as e:
            cli(["fake.enex"])

    assert e.value == fake_exception
    assert "Unhandled exception while parsing note" in caplog.text


def test_file_log(mock_api, fake_note_factory, fs):
    fs.create_file("log.txt")

    cli(["--log", "log.txt", "fake.enex"])

    with open("log.txt") as f:
        done_result = f.read()

    assert "No token provided, dry run mode." in done_result


def test_cli_main_import():
    from enex2notion import __main__
