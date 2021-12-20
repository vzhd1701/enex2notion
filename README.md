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
- Web Clips
  - as plain text or PDFs, see [below](#web-clips)
- Everything else basically

### What is lost

- Paragraph alignment
- Subscript and superscript formatting
- Custom fonts and font sizes
- Tasks
- Encrypted blocks
  - just decrypt them before export

## Installation

[**Download the latest binary release**](https://github.com/vzhd1701/enex2notion/releases/latest) for your OS.

### With PIP

```bash
$ pip install enex2notion
```

**Python 3.6 or later required.**

Or, since **enex2notion** is a standalone tool, it might be more convenient to install it using [**pipx**](https://github.com/pipxproject/pipx):

```shell
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

```shell
$ enex2notion --help
usage: enex2notion [-h] [--token TOKEN] [--mode {DB,PAGE}] [--mode-webclips {TXT,PDF}] [--add-meta] [--done-file FILE] [--verbose] [--version] FILE/DIR [FILE/DIR ...]

Uploads ENEX files to Notion

positional arguments:
  FILE/DIR              ENEX files or directories to upload

optional arguments:
  -h, --help            show this help message and exit
  --token TOKEN         Notion token, stored in token_v2 cookie for notion.so [NEEDED FOR UPLOAD]
  --mode {DB,PAGE}      upload each ENEX as database (DB) or page with children (PAGE) (default: DB)
  --mode-webclips {TXT,PDF}
                        convert web clips to text (TXT) or pdf (PDF) before upload (default: TXT)
  --add-meta            include metadata (created, tags, etc) in notes, makes sense only with PAGE mode
  --done-file FILE      file for uploaded notes hashes to resume interrupted upload
  --verbose             output debug information
  --version             show program's version number and exit
```

### Input

You can pass single `*.enex` files or directories. The program will recursively scan directories for `*.enex` files.

### Token & dry run mode

The upload requires you to have a `token_v2` cookie for the Notion website. For information on how to get it, see [this article](https://vzhd1701.notion.site/Find-Your-Notion-Token-5f57951434c1414d84ac72f88226eede).

The program can run without `--token` provided though. It will not make any network requests without it. Executing a dry run with `--verbose` is an excellent way to check if your `*.enex` files are parsed correctly before uploading.

### Upload continuation

The upload will take some time since each note is uploaded block-by-block, so you'll probably need some way of resuming it. `--done-file` is precisely for that. All uploaded note hashes will be stored there, so the next time you start, the upload will continue from where you left off.

All uploaded notebooks will appear under the automatically created `Evernote ENEX Import` page. The program will mark unfinished notes with `[UNFINISHED UPLOAD]` text in the title. After successful upload, the mark will be removed.

### Upload modes

The `--mode` option allows you to choose how to upload your notebooks: as databases or pages. `DB` mode is the default since Notion itself uses this mode when importing from Evernote. `PAGE` mode makes the tree feel like the original Evernote notebooks hierarchy.

Since `PAGE` mode does not benefit from having separate space for metadata, you can still preserve the note's original meta with the `--add-meta` option. It will attach a callout block with all meta info as a first block in each note [like this](https://imgur.com/a/lJTbprH).

### Web Clips

Due to Notion's limitations Evernote web clips cannot be uploaded as-is. `enex2notion` provides two modes with the `--mode-webclips` option:

- `TXT`, converting them to text, stripping all HTML formatting \[Default\]

  - similar to Evernote's "Simplify & Make Editable"

- `PDF`, converting them to PDF, keeping HTML formatting as close as possible

  - web clips are converted using [wkhtmltopdf](https://wkhtmltopdf.org/), see [this page](https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf) on how to install it

## Examples

### Checking notes before upload

```shell
$ enex2notion --verbose my_notebooks/
```

### Uploading notes from a single notebook

```shell
$ enex2notion --token <YOUR_TOKEN_HERE> "notebook.enex"
```

### Uploading with the option to continue later

```shell
$ enex2notion --token <YOUR_TOKEN_HERE> --done-file done.txt "notebook.enex"
```

## Getting help

If you have a question about the program or have difficulty using it, you are welcome to [the discussions page](https://github.com/vzhd1701/enex2notion/discussions). You can also mail me directly, I'm always happy to help.
