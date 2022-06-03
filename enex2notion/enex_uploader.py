import logging

from notion.block import CollectionViewPageBlock, PageBlock
from notion.collection import CollectionRowBlock
from notion.operations import build_operation
from requests import HTTPError
from tqdm import tqdm

from enex2notion.enex_types import EvernoteNote
from enex2notion.enex_uploader_block import upload_block
from enex2notion.utils_exceptions import NoteUploadFailException

logger = logging.getLogger(__name__)

PROGRESS_BAR_WIDTH = 80


def upload_note(root, note: EvernoteNote, note_blocks):
    logger.debug(f"Creating new page for note '{note.title}'")
    new_page = _make_page(note, root)

    progress_iter = tqdm(
        iterable=note_blocks, unit="block", leave=False, ncols=PROGRESS_BAR_WIDTH
    )

    try:
        for block in progress_iter:
            upload_block(new_page, block)
    except HTTPError as e:
        logger.debug(f"Network error: {e}")
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
