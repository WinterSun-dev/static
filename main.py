from textnode import TextNode
from htmlnode import HTMLNode, ParentNode, LeafNode
import re
import os
import shutil

title = []
def text_to_html(text_node: TextNode):
    match text_node.text_type:
        case "text":
            return LeafNode(None, text_node.text)
        case "bold":
            return LeafNode("b", text_node.text)
        case "italic":
            return LeafNode("i", text_node.text)
        case "code":
            return LeafNode("code", text_node.text)
        case "a":
            return LeafNode("a", text_node.text, **{"href": text_node.url})
        case "img":
            return LeafNode("img", text_node.text, **{"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Invalid text type")


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)]\((.*?)\)", text)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for s in old_nodes:
        if s.text_type != "text":
            new_nodes.append(s)
            continue
        st = s.text
        le_st = len(st)
        le_de = len(delimiter)
        # find all ocurences
        res = [i for i in range(le_st) if st.startswith(delimiter, i)]
        # filtter out "sypbol limiters"
        #    res2 = filter(lambda i: not (i == 0 and st[i] == " ") or not (st[i-1] == "\\"), res)
        #    print(list(res2))
        # test if valid (no unclosed)


        if len(res) % 2 == 1:
            raise ValueError(f"Block didn't close ::: {len(res) =}"
                             f" ::: {res = }")
        if len(res) == 0:
            new_nodes.append(s)
            continue
        sco = 0
        if res[0] != 0:
            sco = 1
            res.insert(0, -le_de)

        if res[-1] != le_st - le_de:
            res.append(le_st)

        # split to nodes (ranges?)
        for r in range(0, len(res) - 1):
            sco += 1
            new_nodes.append(TextNode(st[res[r] + le_de:res[r + 1]], text_type if sco % 2 == 1 else "text"))
    return new_nodes


def split_nodes_image(old_nodes):
    new_nod = []
    for n in old_nodes:
        if n.text_type != "text":
            new_nod.append(n)
            continue
        st = n.text
        len_st = len(st)
        dat = re.findall(r"!\[(.*?)]\((.*?)\)", st)
        sat = re.finditer(r"!\[(.*?)]\((.*?)\)", st)
        start = 0
        for i, r in enumerate(sat):
            if r.span()[0] != start:
                new_nod.append(TextNode(st[start:r.span()[0]], "text", None))

            new_nod.append(TextNode(dat[i][0], "img", dat[i][1]))
            start = r.span()[1]
        if start != len_st:
            new_nod.append(TextNode(st[start:len_st], "text", None))

    return new_nod


def split_nodes_link(old_nodes):
    new_nod = []
    for n in old_nodes:
        if n.text_type != "text":
            new_nod.append(n)
            continue
        st = n.text
        len_st = len(st)
        dat = re.findall(r"\[(.*?)]\((.*?)\)", st)
        sat = re.finditer(r"\[(.*?)]\((.*?)\)", st)
        start = 0
        for i, r in enumerate(sat):
            if r.span()[0] != start:
                new_nod.append(TextNode(st[start:r.span()[0]], "text", None))

            new_nod.append(TextNode(dat[i][0], "a", dat[i][1]))
            start = r.span()[1]
        if start != len_st:
            new_nod.append(TextNode(st[start:len_st], "text", None))

    return new_nod


def markdown_to_blocks(markdown: str):
    sect = markdown.split("\n\n")
    blocs = []
    for s in sect:
        bloc = []
        for l in s.split("\n"):
            if l.strip() != "\n":
                bloc.append(l.strip())

        blocs.append("\n".join(bloc))

    return blocs


def node_splitter(node):
    nod = TextNode(node, "text", None)
    nod = split_nodes_delimiter([nod], "**", "bold")
    nod = split_nodes_delimiter(nod, "*", "italic")
    nod = split_nodes_delimiter(nod, "`", "code")
    nod = split_nodes_image(nod)
    nod = split_nodes_link(nod)
    return nod


def block_to_block_type(block: str):
    spac = block.split(" ", 1)
    lich = block.split("\n", 1)
    bod = spac if len(spac[0])<len(lich[0]) else lich
    match bod[0]:
        case "#":
            title.append(bod[1])
            return bod[1], "h1"
        case "##":
            return bod[1], "h2"
        case "###":
            return bod[1], "h3"
        case "####":
            return bod[1], "h4"
        case "#####":
            return bod[1], "h5"
        case "######":
            return bod[1], "h6"

        case "```":
            print(block)
            return bod[1][:-3], "code"

        case ">":
            new = []
            for b in block.split("\n"):
                if b.split(" ", 1)[0] == ">":
                    new.append(b.split(" ", 1)[1])
                    continue
                return block, "par"
            return "\n".join(new), "qua"

        case "*":
            return f"<li>{bod[1].replace("\n* ", "</li>\n<li>")}</li>", "un_list"

        case "-":
            return f"<li>{bod[1].replace("\n- ", "</li>\n<li>")}</li>", "un_list"

        case "1.":
            new =[]
            for i, l in enumerate(block.split("\n")):
                new.append(f"<li>{l.split(" ", 1)[1]}</li>")

            return "\n".join(new), "or_list"

        case _:
            return block, "par"


def markdown_to_html_node(markdown):
    blocs = markdown_to_blocks(markdown)

    typed_blocs = map(block_to_block_type, blocs)
    # take in document
    # convert to blocks and record types
    node_blocs = []
    for v in typed_blocs:
        bloc_childs = list(map(text_to_html, node_splitter(v[0])))

        #print(f"{bloc_childs =  }")

        node_blocs.append(ParentNode(v[1], None, bloc_childs))

    # convert blok to inline nodes
    text_html = ""
    for n in node_blocs:
        #print(f"{n = }")
        text_html += n.to_html() + "\n"

    text_html = f"<div>{text_html}<div>"

    return text_html


def copy_to_public(dir, copy):
    def rec(src, des):
        for f in os.listdir(src):
            old = os.path.join(src, f)
            new = os.path.join(des, f)
            if os.path.isfile(old):
                shutil.copy(old, des)
                continue
            os.mkdir(new)
            rec(old, new)

    shutil.rmtree(copy, True)
    os.mkdir(copy)
    rec(dir, copy)

def generate_page(from_path, template_path, dest_path):
    with open(from_path) as f:
        mk = f.read()
    with open(template_path) as f:
        tf = f.read()
    htmml = markdown_to_html_node(mk)
    new_html = tf.replace("{{ Title }}", title[0]).replace("{{ Content }}", htmml)
    with open(dest_path, "w") as d:
        d.write(new_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    def rec(src, des):
        for f in os.listdir(src):
            old = os.path.join(src, f)
            new = os.path.join(des, f)
            if os.path.isfile(old):
                if old.split(".")[-1] == "md":
                    print(f"{old = }  :::  {des = }")
                    generate_page(old, template_path, new.replace(".md", ".html"))
                    continue
                shutil.copy(old, des)
                continue
            os.mkdir(new)
            rec(old, new)

    shutil.rmtree(dest_dir_path, True)
    os.mkdir(dest_dir_path)
    rec(dir_path_content, dest_dir_path)

def main():

    copy_to_public("Static", "public")
    generate_pages_recursive("content", "template.html", "public")
   # generate_page("content/majesty/index.md", "template.html", "public/index.html")

if __name__ == '__main__':
    main()
