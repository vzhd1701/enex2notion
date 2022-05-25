import logging

from bs4 import Tag

logger = logging.getLogger(__name__)


def parse_encrypt(element: Tag):
    logger.warning("Skipping encrypted block")
