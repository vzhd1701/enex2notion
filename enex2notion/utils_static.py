from argparse import Namespace
from dataclasses import dataclass
from typing import Optional


@dataclass
class Rules(object):
    mode_webclips: str

    add_meta: bool
    add_pdf_preview: bool
    condense_lines: bool
    condense_lines_sparse: bool

    tag: Optional[str]

    retry: int
    skip_failed: bool
    keep_failed: bool

    @classmethod
    def from_args(cls, args: Namespace) -> "Rules":
        args_map = {
            arg_name: getattr(args, arg_name) for arg_name in cls.__dataclass_fields__
        }

        return cls(**args_map)
