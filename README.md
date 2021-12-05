# enex2notion

[![PyPI version](https://img.shields.io/pypi/v/enex2notion?label=version)](https://pypi.python.org/pypi/enex2notion)
[![Python Version](https://img.shields.io/pypi/pyversions/enex2notion.svg)](https://pypi.org/project/enex2notion/)
[![tests](https://github.com/vzhd1701/enex2notion/actions/workflows/test.yml/badge.svg)](https://github.com/vzhd1701/enex2notion/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/vzhd1701/enex2notion/branch/master/graph/badge.svg)](https://codecov.io/gh/vzhd1701/enex2notion)

Easy way to import [Evernote's](https://www.evernote.com/) `*.enex` files to [Notion.so](https://notion.so)

Notion's native Evernote importer doesn't do it for me, so I decided to write my own. Thanks to **Cobertos** and [md2notion](https://github.com/Cobertos/md2notion) for inspiration and **Jamie Alexandre** for [notion-py](https://github.com/jamalex/notion-py).

You can either use Evernote native export or try out my other tool, [evernote-backup](https://github.com/vzhd1701/evernote-backup), to export `*.enex` files from Evernote.

### What is preserved

- Embedded files and images are uploaded to Notion
  - nested images will appear after paragraph
- Text formatting (**bold**, _italic_, etc) and colors
- Tables are converted to the new format (no colspans though)
- Everything else basically

### What is lost

- Paragraph alignment
- Subscript and superscript formatting
- Custom fonts and font sizes
- Tasks
- Encrypted blocks
  - just decrypt them before export
- Web Clips
  - you'll have better luck converting those to `*.md` and using [md2notion](https://github.com/Cobertos/md2notion)

## Installation

[**Download the latest binary release**](https://github.com/vzhd1701/enex2notion/releases/latest) for your OS.

### With PIP

```bash
$ pip install enex2notion
```

**Python 3.6 or later required.**

Or, since **enex2notion** is a standalone tool, it might be more convenient to install it using [**pipx**](https://github.com/pipxproject/pipx):

```bash
$ pipx install enex2notion
```

### From source

This project uses [poetry](https://python-poetry.org/) for dependency management and packaging. You will have to install it first. See [poetry official documentation](https://python-poetry.org/docs/) for instructions.

```shell
$ git clone https://github.com/vzhd1701/enex2notion.git
$ cd enex2notion/
$ poetry install --no-dev
$ poetry run enex2notion
```

## Usage

```bash
$ enex2notion --help
usage: enex2notion [-h] [--token TOKEN] [--mode {DB,PAGE}] [--add-meta] [--done-file FILE] [--verbose] [--version] FILE/DIR [FILE/DIR ...]

Uploads ENEX files to Notion

positional arguments:
  FILE/DIR          ENEX files or directories to upload

optional arguments:
  -h, --help        show this help message and exit
  --token TOKEN     Notion token, stored in token_v2 cookie for notion.so [NEEDED FOR UPLOAD]
  --mode {DB,PAGE}  upload each ENEX as database (DB) or page with children (PAGE) (default: DB)
  --add-meta        include metadata (created, tags, etc) in notes, makes sense only with PAGE mode
  --done-file FILE  file for uploaded notes hashes to resume interrupted upload
  --verbose         output debug information
  --version         show program's version number and exit
```

You can pass single `*.enex` files or directories. The program will recursively scan directories for `*.enex` files.

The upload requires you to have a `token_v2` cookie for the Notion website. For information on how to get it, see [this article](https://www.notion.so/Find-Your-Notion-Token-5da17a8df27a4fb290e9e3b5d9ba89c4).

The program can run without `--token` provided though. It will not make any network requests without it. Executing a dry run with `--verbose` is an excellent way to check if your `*.enex` files are parsed correctly before uploading.

The upload will take some time since each note is uploaded block-by-block, so you'll probably need some way of resuming it. `--done-file` is precisely for that. All uploaded note hashes will be stored there, so the next time you start, the upload will continue from where you left off.

All uploaded notebooks will appear under the automatically created `Evernote ENEX Import` page. The program will mark unfinished notes with `[UNFINISHED UPLOAD]` text in the title. After successful upload, the mark will be removed.

The `--mode` option allows you to choose how to upload your notebooks: as databases or pages. `DB` mode is the default since Notion itself uses this mode when importing from Evernote. `PAGE` mode makes the tree feel like the original Evernote notebooks hierarchy.

Since `PAGE` mode does not benefit from having separate space for metadata, you can still preserve the note's original meta with the `--add-meta` option. It will attach a callout block with all meta info as a first block in each note.

## Examples

### Checking notes before upload

```shell
$ enex2notion --verbose my_notebooks/
WARNING: No token provided, dry run mode. Nothing will be uploaded to Notion!
INFO: Processing directory 'my_notebooks'...
INFO: Processing notebook 'Test Notebook'...
DEBUG: Parsing note 'Test note 1'
DEBUG: Parsing note 'Test note 2'
DEBUG: Parsing note 'Test note 3'
DEBUG: Parsing note 'Test note with encrypted block'
WARNING: Skipping encrypted block
```

### Uploading notes from a single notebook

```shell
$ enex2notion --token "30d0...9c12" "my_notebooks/Test Notebook.enex"
INFO: 'Evernote ENEX Import' page found
INFO: Processing notebook 'Test Notebook'...
INFO: Creating new page for note 'Test note'
Uploading 'Test note' |####                            | 40/304
```

## Dependencies

- [notion](https://github.com/jamalex/notion-py)
- [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/)
- [python-dateutil](https://github.com/dateutil/dateutil)
- [progress](http://github.com/verigak/progress/)
- [requests](https://github.com/psf/requests)
- [w3lib](https://github.com/scrapy/w3lib)
- [tinycss2](https://github.com/Kozea/tinycss2)
