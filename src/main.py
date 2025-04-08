import os
import shutil
from generatepage import generate_page_recursive

def prepare_public_directory(public_dir):
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    os.mkdir(public_dir)

def map_static_files(directory, static_dir, public_dir):
    if not os.path.exists(directory):
        print(f"Error: '{directory}' directory does not exist.")
        return []

    files_map = []
    for item in os.listdir(directory):
        current_path = os.path.join(directory, item)
        rel_path = os.path.relpath(current_path, start=static_dir)
        dest_path = os.path.join(public_dir, rel_path)

        if os.path.isfile(current_path):
            shutil.copy(current_path, dest_path)
            files_map.append(dest_path)
        else:
            os.makedirs(dest_path, exist_ok=True)
            files_map.extend(map_static_files(current_path, static_dir, public_dir))
    return files_map
    
def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(project_root, "static")
    public_dir = os.path.join(project_root, "public")

    print("Project Root:", project_root)
    print("Static Directory:", static_dir)
    print("Public Directory:", public_dir)

    prepare_public_directory(public_dir)

    files = map_static_files(static_dir, static_dir, public_dir)

    print("Copied files:", files)

    dir_path_content = os.path.join(project_root, "content")
    template_path = os.path.join(project_root, "template.html")
    dest_dir_path = public_dir
    generate_page_recursive(dir_path_content, template_path, dest_dir_path)

if __name__ == "__main__":
    main()