import logging
import sys

from notion.block import PageBlock
from notion.client import NotionClient
from requests import HTTPError, codes

from enex2notion.utils_exceptions import BadTokenException

logger = logging.getLogger(__name__)


def get_root(token, name):
    if not token:
        logger.warning(
            "No token provided, dry run mode. Nothing will be uploaded to Notion!"
        )
        return None

    try:
        client = get_notion_client(token)
    except BadTokenException:
        logger.error("Invalid token provided!")
        sys.exit(1)

    return get_import_root(client, name)


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
