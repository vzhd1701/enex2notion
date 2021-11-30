from bs4 import Tag

from enex2notion.notion_blocks import TextProp
from enex2notion.notion_blocks_table import NotionTableBlock
from enex2notion.string_extractor import extract_string


def parse_table(element):
    rows = _convert_table_into_rows(element)

    table = NotionTableBlock(columns=len(rows[0]))

    for row in rows:
        table.add_row(row)

    return table


def _convert_table_into_rows(table: Tag):
    rows = [
        [extract_string(t_column) for t_column in t_row.find_all("td")]
        for t_row in table.find_all("tr")
    ]

    # pad rows, since notion can't do colspan
    longest_row = max(len(r) for r in rows)
    for row in rows:
        empty_cells = range(longest_row - len(row))
        row.extend([TextProp("") for _ in empty_cells])

    return rows
