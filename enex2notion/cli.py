import logging
import sys
from pathlib import Path
from typing import List

from enex2notion.cli_args import parse_args
from enex2notion.cli_logging import setup_logging
from enex2notion.cli_notion import get_root
from enex2notion.cli_upload import EnexUploader
from enex2notion.cli_wkhtmltopdf import ensure_wkhtmltopdf
from enex2notion.utils_static import Rules

logger = logging.getLogger(__name__)


def cli(argv):
    args = parse_args(argv)

    rules = Rules.from_args(args)

    setup_logging(args.verbose, args.log)

    if rules.mode_webclips == "PDF":
        ensure_wkhtmltopdf()

    root = get_root(args.token, args.root_page)

    enex_uploader = EnexUploader(
        import_root=root, mode=args.mode, done_file=args.done_file, rules=rules
    )

    _process_input(enex_uploader, args.enex_input)


def _process_input(enex_uploader: EnexUploader, enex_input: List[Path]):
    for path in enex_input:
        if path.is_dir():
            logger.info(f"Processing directory '{path.name}'...")
            for enex_file in sorted(path.glob("**/*.enex")):
                enex_uploader.upload_notebook(enex_file)
        else:
            enex_uploader.upload_notebook(path)


def main():  # pragma: no cover
    try:
        cli(sys.argv[1:])
    except KeyboardInterrupt:
        sys.exit(1)
