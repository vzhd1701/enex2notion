import logging
import warnings
from pathlib import Path
from typing import Optional


def setup_logging(is_verbose: bool, log_file: Optional[Path]):
    logging.basicConfig(format="%(levelname)s: %(message)s")

    logging.getLogger("enex2notion").setLevel(
        logging.DEBUG if is_verbose else logging.INFO
    )

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)-8.8s] %(message)s")
        )
        logging.getLogger("enex2notion").addHandler(file_handler)

    logging.getLogger("urllib3").setLevel(logging.ERROR)
    logging.getLogger("notion").setLevel(logging.WARNING)

    _disable_bs4_warning()


def _disable_bs4_warning():  # pragma: no cover
    # For latest version of BeautifulSoup
    try:
        from bs4 import XMLParsedAsHTMLWarning  # noqa: WPS433
    except ImportError:
        return

    warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
