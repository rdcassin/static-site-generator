import os
from markdowntoblocks import markdown_to_html_node
from extractmarkdown import extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        content = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    content_node = markdown_to_html_node(content)
    content_html = content_node.to_html()
    title = extract_title(content)
    titled_template = template.replace("{{ Title }}", title)
    completed_template = titled_template.replace("{{ Content }}", content_html)
    generate_dirs_and_file(dest_path, completed_template)

def generate_dirs_and_file(dest_path, content_html):
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    file_path = os.path.join(dest_path, "index.html")
    with open(file_path, "w") as f:
        f.write(content_html)

def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)
    for item in os.listdir(dir_path_content):
        current_path = os.path.join(dir_path_content, item)
        if os.path.isfile(current_path):
            if current_path.endswith(".md"):
                generate_page(current_path, template_path, dest_dir_path)
        else:
            new_dest_dir = os.path.join(dest_dir_path, item)
            generate_page_recursive(current_path, template_path, new_dest_dir)