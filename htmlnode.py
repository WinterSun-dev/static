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
        return (f"|"
                f"tag={self.tag}, "
                f"value={self.value}, "
                f"children={self.children} !!! , "
                f"props={", ".join(map(lambda x: f'{x[0]}:{x[1]}', self.props.items()))}"
                f"|")


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
                return f"<code>{self.value}</code>"
            case "img": #image
                if self.props["src"] and self.props["alt"]:
                    return f"<img src={self.props["src"]} alt={self.props["alt"]}>"
                raise ValueError("Missing props")

            case _:
                raise ValueError("Tag not recognized")


class ParentNode(HTMLNode):
    def __init__(self, tag, value=None, *children, **props):
        if tag is None:
            raise ValueError("Parent must have tag")
        if not children:
            raise ValueError("Parent must have children")
        #print(f"{children =}")
        #print(f"{type(children) = }")

        super().__init__(tag, value, *children, **props)

    def to_html(self):
        chi = "".join(map(lambda x: x.to_html(), self.children[0]))
        chil = map(lambda x: x.to_html(), self.children[0])
        match self.tag:
            case "par": #paragrapf
                return f"<p>{chi}</p>"

            case "h1": #Header 1
                return f"<h1>{chi}</h1>"
            case "h2": #Header 2
                return f"<h2>{chi}</h2>"
            case "h3": #Header 3
                return f"<h3>{chi}</h3>"
            case "h4": #Header 4
                return f"<h4>{chi}</h4>"
            case "h5": #Header 5
                return f"<h5>{chi}</h5>"
            case "h6": #Header 6
                return f"<h6>{chi}</h6>"
            case "code": #code
                return f"<pre><code>{chi}</code></pre>"
            case "qua": #Quatation
                return f"<blockquote>{chi}</blockquote>"
            case "un_list": #Un oredered list
                #print(chi)
                return f"<ul>{chi}</ul>"
            case "or_list": #Oredered list
                return f"<ol>{chi}</ol>"
            case _:
                raise ValueError("missing or wrong tag")



node = ParentNode(
    "p", None, *[LeafNode("b", "Bold text"), LeafNode(None, "Normal text"), LeafNode("i", "italic text"), LeafNode(None, "Normal text")],
)


#node = LeafNode("p","toimiiko")


