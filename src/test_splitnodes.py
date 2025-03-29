import unittest

from textnode import TextType, TextNode
from splitnodes import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes

class TestSplitNodes(unittest.TestCase):
    def test_eq(self):
        node = TextNode("`code block` This is text with a word", TextType.TEXT)
        new_node = split_nodes_delimiter([node], "`", TextType.CODE)
        node_result = [
            TextNode("code block", TextType.CODE),
            TextNode(" This is text with a word", TextType.TEXT),
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
            TextNode("`code block` This is text with a word", TextType.TEXT),
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        node4 = TextNode("This is text with another _italic block_ word", TextType.TEXT)
        new_node4 = split_nodes_delimiter([node2, node4], "_", TextType.ITALIC)
        node_result4 = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
            TextNode("This is text with another ", TextType.TEXT),
            TextNode("italic block", TextType.ITALIC),
            TextNode(" word", TextType.TEXT)
        ]

        self.assertEqual(new_node, node_result)
        self.assertEqual(new_node2, node_result2)
        self.assertEqual(new_node3, node_result3)
        self.assertEqual(new_node4, node_result4)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_node = split_nodes_image([node])
        node_result = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]
        node2 = TextNode(
            "This is text with two images ![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png) together",
            TextType.TEXT,
        )
        new_node2 = split_nodes_image([node2])
        node_result2 = [
            TextNode("This is text with two images ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            TextNode(" together", TextType.TEXT),
        ]
        new_node3 = split_nodes_image([node, node2])
        node_result3 = node_result + node_result2
        self.assertListEqual(new_node, node_result)
        self.assertListEqual(new_node2, node_result2)
        self.assertListEqual(new_node3, node_result3)

    def test_split_links(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        new_node = split_nodes_link([node])
        node_result = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
        ]
        node2 = TextNode("[to boot dev](https://www.boot.dev) this is text with two links [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        new_node2 = split_nodes_link([node2])
        node_result2 = [
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" this is text with two links ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
        ]
        self.assertListEqual(new_node, node_result)
        self.assertListEqual(new_node2, node_result2)

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_node = text_to_textnodes(text)
        text_result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        text2 = "[link](https://boot.dev) this is `code block` **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_node2 = text_to_textnodes(text2)
        text_result2 = [
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode(" this is ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(new_node, text_result)
        self.assertListEqual(new_node2, text_result2)

if __name__ == "__main__":
    unittest.main()