import logging
import os
import platform
import shutil
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


def ensure_wkhtmltopdf():  # pragma: no cover
    if shutil.which("wkhtmltopdf") is None:
        if platform.system() == "Windows":
            wkhtmltopdf_path = _find_wkhtmltopdf_path()
            if wkhtmltopdf_path and wkhtmltopdf_path.exists():
                logger.debug(f"Found wkhtmltopdf at {wkhtmltopdf_path}")
                os.environ["PATH"] += os.pathsep + str(wkhtmltopdf_path.parent)
                return

        logger.error("You need to install wkhtmltopdf to use --mode-webclips=PDF")
        sys.exit(1)


def _find_wkhtmltopdf_path():  # pragma: no cover
    import winreg  # noqa: WPS433

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\wkhtmltopdf") as key:
            return Path(winreg.QueryValueEx(key, "PdfPath")[0])
    except FileNotFoundError:
        return None
