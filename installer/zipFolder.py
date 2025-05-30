import os
import shutil
from zipfile import ZipFile

def zip_folders_in_current_directory():
    current_dir = os.getcwd()
    zip_dir = os.path.join(current_dir, "zips")

    if not os.path.exists(zip_dir):
        os.makedirs(zip_dir)

    files = os.listdir(current_dir)
    files.remove("zips")

    
    
    for item in files:
        item_path = os.path.join(current_dir, item)
        if os.path.isdir(item_path):
            zip_file_path = os.path.join(zip_dir, f"{item}.zip")
            if os.path.exists(zip_file_path):
                os.remove(zip_file_path)

            zip_file_path = os.path.join(zip_dir, f"{item}.zip")
            with ZipFile(zip_file_path, 'w') as zipf:
                for root, _, files in os.walk(item_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, item_path)
                        zipf.write(file_path, arcname)

if __name__ == "__main__":
    zip_folders_in_current_directory()