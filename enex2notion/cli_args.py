import argparse
from pathlib import Path

from enex2notion.version import __version__

HELP_ARGS_WIDTH = 29


def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog="enex2notion",
        description="Uploads ENEX files to Notion",
        usage="%(prog)s [-h] [--token TOKEN] [OPTION ...] FILE/DIR [FILE/DIR ...]",
        formatter_class=lambda prog: argparse.HelpFormatter(
            prog, max_help_position=HELP_ARGS_WIDTH
        ),
    )

    schema = {
        "enex_input": {
            "type": Path,
            "nargs": "+",
            "help": "ENEX files or directories to upload",
            "metavar": "FILE/DIR",
        },
        "--token": {
            "help": (
                "Notion token, stored in token_v2 cookie for notion.so"
                " [NEEDED FOR UPLOAD]"
            ),
        },
        "--root-page": {
            "default": "Evernote ENEX Import",
            "help": (
                "root page name for the imported notebooks,"
                " it will be created if it does not exist"
                ' (default: "Evernote ENEX Import")'
            ),
            "metavar": "NAME",
        },
        "--mode": {
            "choices": ["DB", "PAGE"],
            "default": "DB",
            "help": (
                "upload each ENEX as database (DB) or page with children (PAGE)"
                " (default: DB)"
            ),
        },
        "--mode-webclips": {
            "choices": ["TXT", "PDF"],
            "default": "TXT",
            "help": (
                "convert web clips to text (TXT) or pdf (PDF) before upload"
                " (default: TXT)"
            ),
        },
        "--add-pdf-preview": {
            "action": "store_true",
            "help": (
                "include preview image with PDF webclips for gallery view thumbnail"
                " (works only with --mode-webclips=PDF)"
            ),
        },
        "--add-meta": {
            "action": "store_true",
            "help": (
                "include metadata (created, tags, etc) in notes,"
                " makes sense only with PAGE mode"
            ),
        },
        "--tag": {
            "help": "add custom tag to uploaded notes",
        },
        "--condense-lines": {
            "action": "store_true",
            "help": (
                "condense text lines together into paragraphs"
                " to avoid making block per line"
            ),
        },
        "--condense-lines-sparse": {
            "action": "store_true",
            "help": "like --condense-lines but leaves gaps between paragraphs",
        },
        "--done-file": {
            "type": Path,
            "metavar": "FILE",
            "help": "file for uploaded notes hashes to resume interrupted upload",
        },
        "--log": {
            "type": Path,
            "metavar": "FILE",
            "help": "file to store program log",
        },
        "--verbose": {
            "action": "store_true",
            "help": "output debug information",
        },
        "--version": {
            "action": "version",
            "version": f"%(prog)s {__version__}",  # noqa: WPS323
        },
    }

    for arg, arg_params in schema.items():
        parser.add_argument(arg, **arg_params)

    return parser.parse_args(argv)
