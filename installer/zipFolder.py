import os
from zipfile import ZipFile

EXCLUDE_DIRS = {".git", "zips", "installer", "build", "dist", "__pycache__"}

def zip_folders_in_current_directory():
    """Create zip files for all folders in the current directory and plugins directory."""
    installer_dir = os.path.dirname(os.path.abspath(__file__))
    zip_dir = os.path.join(installer_dir, "zips")

    os.makedirs(zip_dir, exist_ok=True)

    plugins_dir = os.path.dirname(installer_dir)
    zip_folders(plugins_dir, zip_dir)
    zip_folders(installer_dir, zip_dir)

def zip_folders(source_dir, destination_dir):
    """Zip all folders in source_dir to destination_dir."""
    try:
        folders = [f for f in os.listdir(source_dir) 
                  if os.path.isdir(os.path.join(source_dir, f)) and f not in EXCLUDE_DIRS]
        
        for folder in folders:
            folder_path = os.path.join(source_dir, folder)
            zip_file_path = os.path.join(destination_dir, f"{folder}.zip")
            
            # Remove existing zip file if it exists
            if os.path.exists(zip_file_path):
                os.remove(zip_file_path)
            
            with ZipFile(zip_file_path, 'w') as zipf:
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, folder_path)
                        zipf.write(file_path, arcname)
                        
    except (OSError, IOError) as e:
        print(f"Error processing {source_dir}: {e}")

if __name__ == "__main__":
    zip_folders_in_current_directory()