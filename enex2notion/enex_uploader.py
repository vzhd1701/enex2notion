import logging

from notion.block import CollectionViewPageBlock, PageBlock
from notion.client import NotionClient
from notion.collection import CollectionRowBlock
from notion.operations import build_operation
from progress.bar import Bar
from requests import HTTPError, codes

from enex2notion.enex_types import EvernoteNote
from enex2notion.note_uploader import upload_block

logger = logging.getLogger(__name__)


class NoteUploadFailException(Exception):
    """Exception for when a note fails to upload"""


class BadTokenException(Exception):
    """Exception for when a token is invalid"""


def get_notion_client(token):
    try:
        return NotionClient(token_v2=token)
    except HTTPError as e:  # pragma: no cover
        if e.response.status_code == codes["unauthorized"]:
            raise BadTokenException
        raise


def get_import_root(client, title):
    try:
        top_pages = client.get_top_level_pages()
    except KeyError:  # pragma: no cover
        # Need empty account to test
        top_pages = []

    for page in top_pages:
        if isinstance(page, PageBlock) and page.title == title:
            logger.info(f"'{title}' page found")
            return page

    logger.info(f"Creating '{title}' page...")
    return client.current_space.add_page(title)


def upload_note(root, note: EvernoteNote, note_blocks):
    logger.info(f"Creating new page for note '{note.title}'")
    new_page = _make_page(note, root)

    # Escape % to prevent progress bar crashing
    note_title = note.title.replace("%", "%%")

    try:
        for block in Bar(f"Uploading '{note_title}'").iter(note_blocks):
            upload_block(new_page, block)
    except HTTPError:
        if isinstance(new_page, CollectionRowBlock):
            new_page.remove()
        else:
            new_page.remove(permanently=True)
        raise NoteUploadFailException

    # Set proper name after everything is uploaded
    new_page.title = note.title

    _update_edit_time(new_page, note.updated)


def _update_edit_time(page, date):
    page._client.submit_transaction(  # noqa: WPS437
        build_operation(
            id=page.id,
            path="last_edited_time",
            args=int(date.timestamp() * 1000),
            table=page._table,  # noqa: WPS437
        ),
        update_last_edited=False,
    )


def _make_page(note, root):
    tmp_name = f"{note.title} [UNFINISHED UPLOAD]"

    return (
        root.collection.add_row(
            title=tmp_name,
            url=note.url,
            tags=note.tags,
            created=note.created,
        )
        if isinstance(root, CollectionViewPageBlock)
        else root.children.add_new(PageBlock, title=tmp_name)
    )
