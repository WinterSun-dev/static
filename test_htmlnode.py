import unittest
from htmlnode import HTMLNode

tt = {"href": "https://www.google.com", "target": "_blank"}

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(**tt)
        self.assertEqual(' href="https://www.google.com" target="_blank"', node.props_to_html())


if __name__ == '__main__':
    unittest.main()