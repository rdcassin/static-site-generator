import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.ITALIC)
        node4 = TextNode("This is a text node", TextType.BOLD, "https://www.example.com")
        node5 = TextNode("This is a node", TextType.IMAGE)
        node6 = TextNode("This is a node", TextType.IMAGE)
        node7 = TextNode("This is a node", TextType.LINK, "https://www.example.com")
        self.assertEqual(node, node2)
        self.assertEqual(node5, node6)
        self.assertNotEqual(node2, node3)
        self.assertNotEqual(node, node4)
        self.assertNotEqual(node4, node7)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        node2 = TextNode("This is a bold node", TextType.BOLD)
        html_node2 = text_node_to_html_node(node2)
        node3 = TextNode("This is an italic node", TextType.ITALIC)
        html_node3 = text_node_to_html_node(node3)
        node4 = TextNode("This is a code node", TextType.CODE)
        html_node4 = text_node_to_html_node(node4)
        node5 = TextNode("This is a link node", TextType.LINK, "https://www.google.com")
        html_node5 = text_node_to_html_node(node5)
        node6 = TextNode("Image Alt Text Twitch.TV Link Provided", TextType.IMAGE, "https://www.twitch.tv")
        html_node6 = text_node_to_html_node(node6)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node2.tag, "b")
        self.assertEqual(html_node2.value, "This is a bold node")
        self.assertEqual(html_node3.tag, "i")
        self.assertEqual(html_node3.value, "This is an italic node")
        self.assertEqual(html_node4.tag, "code")
        self.assertEqual(html_node4.value, "This is a code node")
        self.assertEqual(html_node5.tag, "a")
        self.assertEqual(html_node5.value, "This is a link node")
        self.assertEqual(html_node5.props, {"href": "https://www.google.com"})
        self.assertEqual(html_node6.tag, "img")
        self.assertEqual(html_node6.value, "Image Alt Text Twitch.TV Link Provided")
        self.assertEqual(html_node6.props, {"src": "https://www.twitch.tv", "alt":"Image Alt Text Twitch.TV Link Provided"})

if __name__ == "__main__":
    unittest.main()