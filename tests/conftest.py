import base64
import hashlib
import os
import platform
from hashlib import md5

import pytest
from notion.block import PageBlock
from notion.client import NotionClient

from enex2notion.enex_types import EvernoteResource


@pytest.fixture()
def notion_test_page(runner_id):
    client = NotionClient(token_v2=os.environ.get("NOTION_TEST_TOKEN"))

    test_page_title = f"TESTING PAGE {runner_id}"

    for page in client.get_top_level_pages():
        if isinstance(page, PageBlock) and page.title == test_page_title:
            page.remove(permanently=True)

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
def runner_id():
    runner_id = platform.platform() + platform.python_version()
    return hashlib.md5(runner_id.encode("utf-8")).hexdigest()[:8]
