from notion import block


class TextProp(object):
    def __init__(self, text, properties=None):
        self.text = text

        self.properties = [[text]] if properties is None else properties

        if properties is None:
            self.properties = [[text]] if text else []

    def __eq__(self, other):
        return self.text == other.text and self.properties == other.properties

    def __repr__(self):  # pragma: no cover
        return "<{0}> {1}".format(self.__class__.__name__, self.text)


class NotionBaseBlock(object):
    type = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.attrs = {}
        self.properties = {}
        self.children = []

    def __eq__(self, other):
        return (
            self.type == other.type
            and self.attrs == other.attrs
            and self.properties == other.properties
            and self.children == other.children
        )

    def __repr__(self):  # pragma: no cover
        return "<{class_name}> {type} C:{c_count} {attrs}".format(
            class_name=self.__class__.__name__,
            type=self.type,
            c_count=len(self.children),
            attrs=self.attrs,
        )


class NotionTextBased(NotionBaseBlock):
    def __init__(self, text_prop: TextProp = None, **kwargs):
        super().__init__(**kwargs)

        if text_prop:
            self.attrs["title_plaintext"] = text_prop.text
            self.properties["properties.title"] = text_prop.properties


class NotionTextBlock(NotionTextBased):
    type = block.TextBlock


class NotionDividerBlock(NotionBaseBlock):
    type = block.DividerBlock


class NotionBookmarkBlock(NotionBaseBlock):
    type = block.BookmarkBlock

    def __init__(self, url, **kwargs):
        super().__init__(**kwargs)

        self.attrs["link"] = url
