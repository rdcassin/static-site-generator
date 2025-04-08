from enum import Enum
from textnode import text_node_to_html_node
from splitnodes import text_to_textnodes
from htmlnode import HTMLNode, LeafNode, ParentNode

def markdown_to_blocks(markdown):
    markdown = markdown.strip()
    
    blocks = markdown.split("\n\n")
    
    clean_blocks = []
    for block in blocks:
        lines = block.split("\n")
        clean_lines = [line.strip() for line in lines]
        clean_block = "\n".join(clean_lines)
        
        if clean_block:
            clean_blocks.append(clean_block)
    
    return clean_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    lines = block.splitlines()
    
    if not lines:
        return BlockType.PARAGRAPH
    
    if lines[0].startswith("#"):
        parts = lines[0].split(" ", 1)
        if len(parts) > 1 and all(char == '#' for char in parts[0]) and 1 <= len(parts[0]) <= 6:
            return BlockType.HEADING
    
    if len(lines) >= 2 and lines[0] == "```" and lines[-1] == "```":
        return BlockType.CODE
    
    is_quote = True
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE
    
    is_unordered = True
    for line in lines:
        if not line.startswith("- "):
            is_unordered = False
            break
    if is_unordered:
        return BlockType.UNORDERED_LIST
    
    is_ordered = True
    for i, line in enumerate(lines, 1):
        expected_start = f"{i}. "
        if not line.startswith(expected_start):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            block_node = paragraph_to_html_node(block)
        elif block_type == BlockType.HEADING:
            block_node = heading_to_html_node(block)
        elif block_type == BlockType.CODE:
            block_node = code_to_html_node(block)
        elif block_type == BlockType.UNORDERED_LIST:
            block_node = unordered_list_to_html_node(block)
        elif block_type == BlockType.ORDERED_LIST:
            block_node = ordered_list_to_html_node(block)
        elif block_type == BlockType.QUOTE:
            block_node = quote_to_html_node(block)
        else:
            continue
        
        nodes.append(block_node)
    
    parent_node = ParentNode("div", nodes, None)

    return parent_node

def text_to_children(text):
    text_nodes = text_to_textnodes(text)

    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    
    return html_nodes

def paragraph_to_html_node(block):
    split_block = block.split("\n")
    for item in split_block:
        item.strip()
    rejoined_block = " ".join(split_block)
    children = text_to_children(rejoined_block)
    return ParentNode("p", children, None)

def heading_to_html_node(block):
    split_block = block.split()
    level = 0
    for char in split_block[0]:
        if char == '#':
            level += 1
        else:
            break
    
    content = block[level:].strip()
    
    children = text_to_children(content)
    return ParentNode(f"h{level}", children, None)

def code_to_html_node(block):
    stripped_content = block.strip("`").lstrip("\n")
    return ParentNode("pre", [LeafNode("code", stripped_content, None)], None)

def unordered_list_to_html_node(block):
    items = block.split("\n")
    children = []
    for item in items:
        if item:
            stripped_item = item.lstrip("- ")
            content = text_to_children(stripped_item.strip())
            child = ParentNode("li", content, None)
            children.append(child)
    return ParentNode("ul", children, None)

def ordered_list_to_html_node(block):
    items = block.split("\n")
    children = []
    for item in items:
        if item:
            split_item = item.split(" ", 1)
            content = text_to_children(split_item[1].strip())
            child = ParentNode("li", content, None)
            children.append(child)
    return ParentNode("ol", children, None)

def quote_to_html_node(block):
    lines = block.split("\n")
    children = []
    for line in lines:
        if line.strip():
            clean_line = line.lstrip("> ").strip()
            children.append(clean_line)
    rejoined_block = " ".join(children)
    child_nodes = text_to_children(rejoined_block)
    return ParentNode("blockquote", child_nodes, None)