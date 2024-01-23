import os
import shutil
from config import paths, target_dir

def copy_odt_files():
    # Check if target directory exists, if not, create it
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"Created target directory at: {target_dir}")

    # Loop through each folder
    for path in paths:
        # Check if folder exists
        if not os.path.exists(path):
            print(f"Folder {path} not found, skipping...")
            continue
        
        # Loop through each file in the folder
        for file_name in os.listdir(path):
            # Check if the file is an .odt file
            # print(f"File name: {file_name}")
            if file_name.endswith('.odt') or file_name.endswith('.docx'):
                # Construct full file path
                file_path = os.path.join(path, file_name)
                # Construct destination file path
                dest_path = os.path.join(target_dir, file_name)
                # Copy the file to the target directory
                try:
                    shutil.copy(file_path, dest_path)
                    print(f"Copied {file_path} to {dest_path}")
                except Exception as e:
                    print(f"Failed to copy {file_path} to {dest_path}, error: {e}")
                


try:
    copy_odt_files()
except Exception as e:
    print(f"An error occurred: {e}")