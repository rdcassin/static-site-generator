import unittest

from textnode import TextType, TextNode
from splitnodes import split_nodes_delimiter

class TestSplitNodes(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "`", TextType.CODE)
        node_result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        node2 = TextNode("This is text with an _italic block_ word", TextType.TEXT)
        new_node2 = split_nodes_delimiter([node2], "_", TextType.ITALIC)
        node_result2 = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        new_node3 = split_nodes_delimiter([node, node2], "_", TextType.ITALIC)
        node_result3 = [
            [TextNode("This is text with a `code block` word", TextType.TEXT)],
            [TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),]
        ]
        node4 = TextNode("This is text with another _italic block_ word", TextType.TEXT)
        new_node4 = split_nodes_delimiter([node2, node4], "_", TextType.ITALIC)
        node_result4 = [
            [TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),],
            [TextNode("This is text with another ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),]
        ]

        self.assertEqual(new_node, node_result)
        self.assertEqual(new_node2, node_result2)
        self.assertEqual(new_node3, node_result3)
        self.assertEqual(new_node4, node_result4)

if __name__ == "__main__":
    unittest.main()