class HTMLNode:
    def __init__(self, tag=None, value=None, *children, **props):
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props or {}

    def to_html(self):
        raise NotImplemented
    def __tagger(self, ):
        pass
    def props_to_html(self):
        return "".join(map(lambda x: f' {x[0]}="{x[1]}"', self.props.items()))

    def __repr__(self):
        return (f"tag={self.tag}, "
                f"value={self.value}, "
                f"children={", ".join(self.children)}, "
                f"props={", ".join(map(lambda x: f'{x[0]}:{x[1]}', self.props.items()))}")


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, *children, **props):
        if children:
            raise ValueError("Leaf can't have children")
        if value is None:
            raise ValueError("Must have value")
        super().__init__(tag, value, **props)
        if self.value is None:
            raise ValueError("Must have value")


    def to_html(self):
        match self.tag:
            case None: #normal text
                return self.value
            case "a": #hyperlink
                return f"<a{self.props_to_html()}>{self.value}</a>"
            case "p": #paragraph
                return f"<p>{self.value}</p>"
            case "b": #bold
                return f"<b>{self.value}</b>"
            case "i": #italic
                return f"<i>{self.value}</i>"
            case "code": #code
                return f"<code>{self.value}"
            case "img": #image
                if self.props["src"] and self.props["alt"]:
                    return f"<img src={self.props["src"]} alt={self.props["alt"]}"
                raise ValueError("Missing props")

            case _:
                raise ValueError("Tag not recognized")


class ParentNode(HTMLNode):
    def __init__(self, tag, value=None, *children, **props):
        if tag is None:
            raise ValueError("Parent must have tag")
        if not children:
            raise ValueError("Parent must have children")
        super().__init__(tag, value, *children, **props)

    def to_html(self):
        chi = "".join(map(lambda x: x.to_html(), self.children))
        match self.tag:
            case None: #normal text
                return chi
            case "a": #hyperlink
                return f"<a{self.props_to_html()}>{chi}</a>"
            case "p": #paragraph
                return f"<p>{chi}</p>"
            case "b": #bold
                return f"<b>{chi}</b>"
            case "i": #italic
                return f"<i>{chi}</i>"
            case "code": #code
                return f"<code>{chi}"
            case "img": #image
                if self.props["src"] and self.props["alt"]:
                    return f"<img src={self.props["src"]} alt={self.props["alt"]}"
                raise ValueError("Missing props")

            case _:
                raise ValueError("Tag not recognized")



node = ParentNode(
    "p", None, *[LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text")],
)


#node = LeafNode("p","toimiiko")
print(str(node.to_html()))

