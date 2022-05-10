import base64
import hashlib
import json
import os
import platform
import uuid
from hashlib import md5
from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from notion.block import PageBlock
from notion.client import NotionClient

from enex2notion.enex_types import EvernoteResource


@pytest.fixture(scope="module")
def vcr_config():
    """Remove meta bloat to reduce cassette size"""

    def response_cleaner(response):
        bloat_headers = [
            "Content-Security-Policy",
            "Expect-CT",
            "ETag",
            "Referrer-Policy",
            "Strict-Transport-Security",
            "Vary",
            "Date",
            "Server",
            "Connection",
            "Set-Cookie",
        ]

        for h in response["headers"].copy():
            if h.startswith("X-") or h.startswith("CF-") or h in bloat_headers:
                response["headers"].pop(h)

        return response

    return {
        "filter_headers": [
            ("cookie", "PRIVATE"),
            "Accept",
            "Accept-Encoding",
            "Connection",
            "User-Agent",
        ],
        "before_record_response": response_cleaner,
        "decode_compressed_response": True,
    }


@pytest.fixture()
def vcr_uuid4(mocker, vcr_cassette_dir, vcr_cassette_name):
    uuid_casette_path = Path(vcr_cassette_dir) / f"{vcr_cassette_name}.uuid4.json"

    if uuid_casette_path.exists():
        with open(uuid_casette_path, "r") as f:
            uuid_casette = [uuid.UUID(u) for u in json.load(f)]

        mocker.patch("uuid.uuid4", side_effect=uuid_casette)
    else:
        uuid_casette = []

        orign_uuid4 = uuid.uuid4

        def uuid4():
            u = orign_uuid4()
            uuid_casette.append(u)
            return u

        mocker.patch("uuid.uuid4", side_effect=uuid4)

    yield

    if not uuid_casette_path.exists() and uuid_casette:
        uuid_casette_path.parent.mkdir(parents=True, exist_ok=True)

        with open(uuid_casette_path, "w") as f:
            json.dump([str(u) for u in uuid_casette], f)


@pytest.fixture()
def notion_test_page(vcr_cassette_dir, vcr_cassette_name):
    casette_path = Path(vcr_cassette_dir) / f"{vcr_cassette_name}.yaml"

    # if cassette exists and no token, probably CI test
    if casette_path.exists() and not os.environ.get("NOTION_TEST_TOKEN"):
        token = "fake_token"
    else:
        token = os.environ.get("NOTION_TEST_TOKEN")

    if not token:
        raise RuntimeError(
            "No token found. Set NOTION_TEST_TOKEN environment variable."
        )

    client = NotionClient(token_v2=token)

    test_page_title = f"TESTING PAGE"

    try:
        top_pages = client.get_top_level_pages()
    except KeyError:  # pragma: no cover
        # Need empty account to test
        top_pages = []

    for page in top_pages.copy():
        try:
            if page.title == test_page_title:
                page.remove(permanently=True)
        except AttributeError:
            page.remove(permanently=True)

    if top_pages:
        raise RuntimeError("Testing requires empty account")

    page = client.current_space.add_page(test_page_title)

    yield page

    page.remove(permanently=True)


@pytest.fixture()
def smallest_gif():
    gif_bin = base64.b64decode("R0lGODlhAQABAAAAACH5BAEAAAAALAAAAAABAAEAAAIA")
    gif_md5 = md5(gif_bin).hexdigest()

    return EvernoteResource(
        data_bin=gif_bin,
        size=len(gif_bin),
        md5=gif_md5,
        mime="image/gif",
        file_name="smallest.gif",
    )


@pytest.fixture()
def smallest_svg():
    svg_bin = b"<svg xmlns='http://www.w3.org/2000/svg'>"
    svg_md5 = md5(svg_bin).hexdigest()

    return EvernoteResource(
        data_bin=svg_bin,
        size=len(svg_bin),
        md5=svg_md5,
        mime="image/svg+xml",
        file_name="smallest.svg",
    )


@pytest.fixture()
def tiny_file():
    bin = b"0"
    bin_md5 = md5(bin).hexdigest()

    return EvernoteResource(
        data_bin=bin,
        size=len(bin),
        md5=bin_md5,
        mime="application/octet-stream",
        file_name="tiny.bin",
    )


@pytest.fixture()
def tiny_exe_file():
    bin = b"0"
    bin_md5 = md5(bin).hexdigest()

    return EvernoteResource(
        data_bin=bin,
        size=len(bin),
        md5=bin_md5,
        mime="application/x-msdownload",
        file_name="tiny.exe",
    )


@pytest.fixture()
def parse_html():
    def inner(html):
        return BeautifulSoup(html, "html.parser")

    return inner
