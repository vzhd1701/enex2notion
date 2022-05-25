from notion import block

from enex2notion.notion_blocks.base import NotionBaseBlock


def _lstrip_properties(properties):
    strip_properties = []

    for i, prop in enumerate(properties):
        if not prop[0].strip():
            continue

        if len(prop) == 1:
            strip_properties.append([prop[0].lstrip()])
        else:
            strip_properties.append([prop[0].lstrip(), prop[1]])

        strip_properties.extend(properties[i + 1 :])

        break

    return strip_properties


def _rstrip_properties(properties):
    strip_properties = []

    for i, prop in sorted(enumerate(properties), reverse=True):
        if not prop[0].strip():
            continue

        strip_properties.extend(properties[:i])

        if len(prop) == 1:
            strip_properties.append([prop[0].rstrip()])
        else:
            strip_properties.append([prop[0].rstrip(), prop[1]])

        break

    return strip_properties


class TextProp(object):
    def __init__(self, text, properties=None):
        self.text = text

        self.properties = [[text]] if properties is None else properties

        if properties is None:
            self.properties = [[text]] if text else []

    def strip(self):
        strip_properties = _rstrip_properties(_lstrip_properties(self.properties))

        return TextProp(text=self.text.strip(), properties=strip_properties)

    def __eq__(self, other):
        return self.text == other.text and self.properties == other.properties

    def __repr__(self):  # pragma: no cover
        return "<{0}> {1}".format(self.__class__.__name__, self.text)


class NotionTextBased(NotionBaseBlock):
    def __init__(self, text_prop: TextProp = None, **kwargs):
        super().__init__(**kwargs)

        if text_prop:
            self.attrs["title_plaintext"] = text_prop.text
            self.properties["properties.title"] = text_prop.properties
        else:
            self.attrs["title_plaintext"] = ""
            self.properties["properties.title"] = []

    @property
    def text_prop(self):
        return TextProp(
            text=self.attrs["title_plaintext"],
            properties=self.properties["properties.title"],
        )

    @text_prop.setter
    def text_prop(self, text_prop: TextProp):
        self.attrs["title_plaintext"] = text_prop.text
        self.properties["properties.title"] = text_prop.properties


class NotionTextBlock(NotionTextBased):
    type = block.TextBlock
