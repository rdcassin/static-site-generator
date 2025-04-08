import unittest

from block import markdown_to_blocks, markdown_to_html_node

class TestExtractMarkdownText(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_paragraphs(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quote(self):
        md = """
        > This is a quote.
        > This is a quote with **bolded** text.
        > This is a quote with _italic_ text.
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote. This is a quote with <b>bolded</b> text. This is a quote with <i>italic</i> text.</blockquote></div>",
        )

    def test_heading(self):
        md = """
        # This is Heading 1 with **bolded** and _italic_ text.
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is Heading 1 with <b>bolded</b> and <i>italic</i> text.</h1></div>",
        )

    def test_unordered_list(self):
        md = """
        - Item 1
        - Item 2
        - Item 3
        - Item 4
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li><li>Item 4</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
        1. Item 1
        2. Item 2
        3. Item 3
        4. Item 4
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li><li>Item 4</li></ol></div>",
        )
        
if __name__ == "__main__":
    unittest.main()