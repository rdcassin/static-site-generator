import unittest

from extractmarkdown import extract_markdown_images, extract_markdown_links

class TestExtractMarkdownText(unittest.TestCase):
    def test_eq(self):
        img_extract = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        link_extract = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], img_extract)
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], link_extract)
        
if __name__ == "__main__":
    unittest.main()