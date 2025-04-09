import os
import shutil
import sys
from generatepage import generate_page_recursive

def prepare_page_directory(docs_dir):
    if os.path.exists(docs_dir):
        shutil.rmtree(docs_dir)
    os.mkdir(docs_dir)

def map_static_files(directory, static_dir, docs_dir):
    if not os.path.exists(directory):
        print(f"Error: '{directory}' directory does not exist.")
        return []

    files_map = []
    for item in os.listdir(directory):
        current_path = os.path.join(directory, item)
        rel_path = os.path.relpath(current_path, start=static_dir)
        dest_path = os.path.join(docs_dir, rel_path)

        if os.path.isfile(current_path):
            shutil.copy(current_path, dest_path)
            files_map.append(dest_path)
        else:
            os.makedirs(dest_path, exist_ok=True)
            files_map.extend(map_static_files(current_path, static_dir, docs_dir))
    return files_map
    
def main():

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(project_root, "static")
    # Uncomment the following line to use public directory.  Also change references from public_dir to basepath
    # public_dir = os.path.join(project_root, "public")
    docs_dir = os.path.join(project_root, "docs")

    # print("Project Root:", project_root)
    # print("Static Directory:", static_dir)
    # print("Public Directory:", public_dir)

    prepare_page_directory(docs_dir)

    files = map_static_files(static_dir, static_dir, docs_dir)

    print("Copied files:", files)

    dir_path_content = os.path.join(project_root, "content")
    template_path = os.path.join(project_root, "template.html")
    dest_dir_path = docs_dir
    generate_page_recursive(dir_path_content, template_path, dest_dir_path, basepath)

if __name__ == "__main__":
    main()