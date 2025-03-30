import os
import shutil

def prepare_public_directory(public_dir):
    """Clear and recreate the public directory."""
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)  # Remove the existing directory
    os.mkdir(public_dir)  # Create a fresh directory

def map_static_files(directory, static_dir, public_dir):
    """Recursively map and copy files from static_dir to public_dir."""
    if not os.path.exists(directory):
        print(f"Error: '{directory}' directory does not exist.")
        return []

    files_map = []
    for item in os.listdir(directory):
        current_path = os.path.join(directory, item)
        rel_path = os.path.relpath(current_path, start=static_dir)
        dest_path = os.path.join(public_dir, rel_path)

        if os.path.isfile(current_path):
            # Copy file to destination
            shutil.copy(current_path, dest_path)
            files_map.append(dest_path)  # Track copied files
        else:
            # Create directory before recursion
            os.makedirs(dest_path, exist_ok=True)
            files_map.extend(map_static_files(current_path, static_dir, public_dir))  # Recurse on subdirs
    return files_map

def main():
    # Dynamically calculate paths based on script location
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    static_dir = os.path.join(project_root, "static")
    public_dir = os.path.join(project_root, "public")

    print("Project Root:", project_root)
    print("Static Directory:", static_dir)
    print("Public Directory:", public_dir)

    # Prepare the public directory
    prepare_public_directory(public_dir)

    # Recursively map and copy files
    files = map_static_files(static_dir, static_dir, public_dir)

    print("Copied files:", files)

if __name__ == "__main__":
    main()