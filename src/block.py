from enum import Enum

def markdown_to_blocks(markdown):
    old_blocks = markdown.split("\n\n")
    new_blocks = []
    for old_block in old_blocks:
        split_block = old_block.split("\n", 1)
        starting_text = split_block[0].strip()
        ending_text = split_block[1].strip()
        if starting_text and ending_text:
            ending_text = "\n" + ending_text
        new_block = starting_text + ending_text
        new_blocks.append(new_block)

    return new_blocks

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
    