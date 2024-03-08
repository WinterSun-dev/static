import unittest
from htmlnode import HTMLNode, LeafNode

tt = {"href": "https://www.google.com", "target": "_blank"}

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(**tt)
        self.assertEqual(' href="https://www.google.com" target="_blank"', node.props_to_html())

    def test_leafnode(self):
        node = LeafNode(value="toimii", tag="p")



if __name__ == '__main__':
    unittest.main()