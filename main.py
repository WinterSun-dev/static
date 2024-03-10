from textnode import TextNode
from htmlnode import HTMLNode, ParentNode, LeafNode



def text_to_html(text_node:TextNode):
    match text_node.text_type:
        case "text":
            return LeafNode(None, text_node.text)
        case "bold":
            return LeafNode("b", text_node.text)
        case "italic":
            return LeafNode("i", text_node.text)
        case "code":
            return LeafNode("code", text_node.text)
        case "link":
            return LeafNode("a", text_node.text, **{"href": text_node.url})
        case "image":
            return LeafNode("img", None, **{"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Invalid text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):







def main ():



    print(text_to_html(TextNode("This is a text node", "bold", "https://www.boot.dev")))

    node = TextNode("This is text with a `code block` word", "text")
    new_nodes = split_nodes_delimiter([node], "`", "code")


if __name__ == '__main__':
    main()
