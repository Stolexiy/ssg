import unittest

from htmlnode import HTMLNode


class TestHtmlNode(unittest.TestCase):
    def test_props_single(self):
        attr = HTMLNode("div", "Test text", None, {"class": "test-text"}).props_to_html()
        self.assertEqual(attr, "class=\"test-text\"")

    def test_props_multi(self):
        attr = HTMLNode("div", "Test text", None, {"class": "test-text", "ref": "boot.dev"}).props_to_html()
        self.assertEqual(attr, "class=\"test-text\" ref=\"boot.dev\"")

    def test_props_empty(self):
        attr = HTMLNode("div", "Test text").props_to_html()
        self.assertEqual(attr, "")

if __name__ == "__main__":
    unittest.main()
