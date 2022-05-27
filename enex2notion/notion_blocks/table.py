from typing import Iterable

from notion.block import BasicBlock

from enex2notion.notion_blocks.base import NotionBaseBlock
from enex2notion.notion_blocks.text import TextProp
from enex2notion.utils_rand_id import rand_id_list


class TableBlock(BasicBlock):
    _type = "table"


class TableRowBlock(BasicBlock):
    _type = "table_row"


class NotionTableBlock(NotionBaseBlock):
    type = TableBlock

    def __init__(self, columns: int, **kwargs):
        super().__init__(**kwargs)

        self._columns = rand_id_list(columns, 4)

        self.properties["format.table_block_column_order"] = self._columns

    def add_row(self, row: Iterable[TextProp]):
        t_row = NotionTableRowBlock()

        for col_id, cell in zip(self._columns, row):
            t_row.properties[f"properties.{col_id}"] = cell.properties

        self.children.append(t_row)

    def iter_rows(self):
        yield from (
            [row.properties[f"properties.{col_id}"] for col_id in self._columns]
            for row in self.children
        )


class NotionTableRowBlock(NotionBaseBlock):
    type = TableRowBlock
