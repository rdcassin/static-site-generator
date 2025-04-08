import re

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_title(markdown):
    lines = markdown.splitlines("\n\n")
    content = ""
    for line in lines:
        current_line = line.strip()
        if current_line.startswith("# "):
            content = current_line[2:].strip()
    if content == "":
        raise Exception("No Title Found.")
    return content