from textnode import TextType, TextNode
from extractmarkdown import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        remaining_text= text

        while delimiter in remaining_text:
            split_result = remaining_text.split(delimiter, 1)
            before = split_result[0]
            
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            
            after_opening = split_result[1]
            if delimiter not in after_opening:
                raise Exception(f"Invalid Markdown syntax: missing closing delimiter {delimiter}")
            
            split_result = after_opening.split(delimiter, 1)
            content = split_result[0]
            remaining_text = split_result[1]
            
            new_nodes.append(TextNode(content, text_type))
        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        delimiters = extract_markdown_images(old_node.text)
        text = old_node.text
        remaining_text = text

        for delimiter in delimiters:
            alt_text, url = delimiter
            split_result = remaining_text.split(f"![{alt_text}]({url})", 1)
            text_before = split_result[0]
            
            if text_before:
                new_nodes.append(TextNode(text_before, TextType.TEXT))
            
            remaining_text = split_result[1]
            
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        delimiters = extract_markdown_links(old_node.text)
        text = old_node.text
        remaining_text = text

        for delimiter in delimiters:
            alt_text, url = delimiter
            split_result = remaining_text.split(f"[{alt_text}]({url})", 1)
            text_before = split_result[0]
            
            if text_before:
                new_nodes.append(TextNode(text_before, TextType.TEXT))
            
            remaining_text = split_result[1]
            
            new_nodes.append(TextNode(alt_text, TextType.LINK, url))
        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes

def text_to_textnodes(text):
    input_node = TextNode(text, TextType.TEXT)
    current_node = [input_node]
    text_types = [("**", TextType.BOLD), ("_", TextType.ITALIC), ("`", TextType.CODE),]
    for text_type in text_types:
        altered_node = split_nodes_delimiter(current_node, text_type[0], text_type[1])
        current_node = altered_node
    altered_node = split_nodes_image(current_node)
    current_node = altered_node
    altered_node = split_nodes_link(current_node)
    current_node = altered_node

    return current_node