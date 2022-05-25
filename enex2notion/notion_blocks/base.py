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
