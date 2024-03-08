class HTMLNode:
    def __init__(self, tag=None, value=None, *children, **props):
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props or {}

    def to_html(self):
        raise NotImplemented
    def props_to_html(self):
        return "".join(map(lambda x: f' {x[0]}="{x[1]}"', self.props.items()))

    def __repr__(self):
        return (f"tag={self.tag}, "
                f"value={self.value}, "
                f"children={", ".join(self.children)}, "
                f"props={", ".join(map(lambda x: f'{x[0]}:{x[1]}', self.props.items()))}")

    def tagger(self):
        match self.tag:
            case "a": #hyperlink
                return f"<a{self.props_to_html()}>{self.value}</a>"
            case "p": #paragraph
                return f"<p>{self.value}</p>"
            case "b": #bold
                return f"<b>{self.value}</b>"
            case "i": #italic
                return f"<i>{self.value}</i>"

            case _:
                raise ValueError("Tag not recognized")


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, *children, **props):
        if children:
            raise ValueError("Leaf can't have children")
        if value is None:
            raise ValueError("Must have value")
        super().__init__(tag=tag, value=value, *children, **props)
        if self.value is None:
            raise ValueError("Must have value")


    def to_html(self):
        if self.tag is None:
            return self.value
        return self.tagger()


class ParentNode(HTMLNode):
    def __init__(self, tag, value=None, *children, **props):
        if tag is None:
            raise ValueError("Parent must have tag")
        if not children:
            raise ValueError("Parent must have children")
        super().__init__(tag=tag, value=value, *children, **props)

    def to_html(self):
        return "".join(map(lambda x: x.to_html, self.children))


node = ParentNode(
    "p", None, *[LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text")],
)


#node = LeafNode("p","toimiiko")
print(node.to_html())
