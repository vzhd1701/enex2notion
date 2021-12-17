from notion.block import CollectionViewPageBlock, PageBlock

from enex2notion.rand_id import rand_id_list


def get_notebook_page(root, title):
    existing = _get_existing_notebook_page(root, title)
    if existing is not None:
        return existing

    return root.children.add_new(PageBlock, title=title)


def _get_existing_notebook_page(root, title):
    child_match = (
        c for c in root.children if isinstance(c, PageBlock) and c.title == title
    )

    return next(child_match, None)


def get_notebook_database(root, title):
    _cleanup_empty_databases(root)

    existing = _get_existing_notebook_database(root, title)
    if existing is not None:
        return existing

    schema = _make_notebook_db_schema()

    # Show only Tags and Updated
    properties_order = _properties_order(schema, "Tags", "Updated")

    cvb = root.children.add_new(CollectionViewPageBlock)
    cvb.collection = cvb._client.get_collection(  # noqa: WPS437
        cvb._client.create_record(  # noqa: WPS437
            "collection", parent=cvb, schema=schema
        )
    )

    view = cvb.views.add_new(view_type="list")

    # Set properties display order and visibility options
    view.set("format.list_properties", properties_order)
    cvb.collection.set("format.collection_page_properties", properties_order)

    cvb.title = title

    return cvb


def _make_notebook_db_schema():
    col_ids = rand_id_list(4, 4)
    return {
        col_ids[0]: {"name": "Tags", "type": "multi_select", "options": []},
        col_ids[1]: {"name": "URL", "type": "url"},
        col_ids[2]: {"name": "Created", "type": "created_time"},
        col_ids[3]: {"name": "Updated", "type": "last_edited_time"},
        "title": {"name": "Title", "type": "title"},
    }


def _get_existing_notebook_database(root, title):
    child_match = (
        c
        for c in root.children
        if isinstance(c, CollectionViewPageBlock) and c.title == title
    )

    child = next(child_match, None)
    if child is None:
        return None

    # Make sure options has at least empty list, otherwise it will crash
    tag_col_id = next(
        c_k
        for c_k, c_v in child.collection.get("schema").items()
        if c_v["name"] == "Tags"
    )

    if child.collection.get(f"schema.{tag_col_id}.options") is None:
        child.collection.set(f"schema.{tag_col_id}.options", [])

    return child


def _cleanup_empty_databases(root):
    collections = (c for c in root.children if isinstance(c, CollectionViewPageBlock))

    for c in collections:
        if c.collection is None or not c.title:
            c.remove(permanently=True)


def _properties_order(schema, *fields):
    return [
        {"property": col_id, "visible": col["name"] in fields}
        for col_id, col in schema.items()
        if col_id != "title"
    ]
