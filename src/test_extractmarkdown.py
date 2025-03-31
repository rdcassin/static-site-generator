import unittest

from extractmarkdown import extract_markdown_images, extract_markdown_links, extract_title

class TestExtractMarkdownText(unittest.TestCase):
    def test_eq(self):
        img_extract = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        link_extract = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], img_extract)
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], link_extract)
        
    def test_extract_title(self):
        text = "# Hello   "
        extract_text = extract_title(text)
        text_result = "Hello"
        text2 = "Should not work."
        with self.assertRaises(Exception) as extract_text2 :
            extract_title(text2)
        text_result2 = "Not header 1"
        text3 = "    # Salutations To All! ! !   "
        extract_text3 = extract_title(text3)
        text_result3 = "Salutations To All! ! !"
        text4 = "    ### Salutations   "
        with self.assertRaises(Exception) as extract_text4 :
            extract_title(text4)
        text_result4 = "Not header 1"
        self.assertEqual(extract_text, text_result)
        self.assertEqual(str(extract_text2.exception), text_result2)
        self.assertEqual(extract_text3, text_result3)
        self.assertEqual(str(extract_text4.exception), text_result4)

if __name__ == "__main__":
    unittest.main()