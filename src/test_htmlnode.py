import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_HTMLNode(self):
        node = HTMLNode("a", "placeholder text", None, {"href": "https://www.google.com"})
        node2 = HTMLNode("p", "placeholder text", {"href": "https://www.google.com"})
        node3 = HTMLNode("h1", None, "<span>Some text</span>", {"href": "https://www.google.com"})
        self.assertEqual(str(node), "HTMLNode(Tag: a, Value: placeholder text, Children: None, Props: {'href': 'https://www.google.com'})")
        self.assertNotEqual(node, node2)
        self.assertEqual(str(node3), "HTMLNode(Tag: h1, Value: None, Children: <span>Some text</span>, Props: {'href': 'https://www.google.com'})")

    def test_LeafNode(self):
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("a", "Link to Google", {"href": "https://www.google.com"})
        node3 = LeafNode(None, "Some plain text")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Link to Google</a>')
        self.assertEqual(node3.to_html(), "Some plain text")

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

    def test_to_html_with_multiple_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node2 = LeafNode("h1", "grandchild2")
        child_node = ParentNode("span", [grandchild_node, grandchild_node2])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b><h1>grandchild2</h1></span></div>",
        )

    def test_to_html_with_multiple_children_and_multiple_grandchildren_and_greatgrandchild(self):
        greatgrandchild_node = LeafNode("p", "greatgrandchild", )
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node2 = LeafNode("h1", "grandchild2")
        grandchild_node3 = ParentNode("b", [greatgrandchild_node], {"className": "flex flex-col"})
        child_node = ParentNode("span", [grandchild_node, grandchild_node2])
        child_node2 = LeafNode("h2", "child2")
        child_node3 = ParentNode("span", [grandchild_node, grandchild_node3])
        parent_node = ParentNode("div", [child_node, child_node2])
        parent_node2 = ParentNode("div", [child_node, child_node2, child_node3])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b><h1>grandchild2</h1></span><h2>child2</h2></div>",
        )
        self.assertEqual(
            parent_node2.to_html(),
            '<div><span><b>grandchild</b><h1>grandchild2</h1></span><h2>child2</h2><span><b>grandchild</b><b className="flex flex-col"><p>greatgrandchild</p></b></span></div>'
        )

if __name__ == "__main__":
    unittest.main()