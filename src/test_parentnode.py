import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multi_children(self):
        grandchild_node1 = LeafNode("b", "grandchild1")
        child_node1 = ParentNode("span", [grandchild_node1])
        grandchild_node21 = LeafNode("b", "grandchild21")
        grandchild_node22 = LeafNode("b", "grandchild22")
        child_node2 = ParentNode("span", [grandchild_node21, grandchild_node22])
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild1</b></span><span><b>grandchild21</b><b>grandchild22</b></span></div>",
        )

    def test_to_html_with_no_children(self):
        ParentNode("div", [])
        self.assertRaises(ValueError)

if __name__ == "__main__":
    unittest.main()
