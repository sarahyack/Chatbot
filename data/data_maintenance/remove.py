# data\data_maintenance\remove.py

"""
This module contains functions for data maintenance.

Functions include:
    - delete_db(path: str, delete_existing_db: bool = True)
        Delete the database file.

"""
import os

from file_setup import config


def delete_db(path, delete_existing_db=True):
    if os.path.exists(path) and os.path.isfile(path) and delete_existing_db:
        user_input: str = input(
            "Database file already exists. Do you want to overwrite it? Action cannot be undone. (y/n): ")
        if user_input.lower() != "y":
            print("Database file not overwritten.")
            with open(config.log_path, "a") as f:
                f.write("Database file not overwritten.\n")
            return
        else:
            try:
                if os.access(path, os.W_OK):
                    print(f"Database file {path} is writable. Attempting to delete...")
                    os.remove(path)
                    print(f"Database file deleted: {path}")
                    with open(config.log_path, "a") as f:
                        f.write(f"Database file deleted: {path}\n")
                else:
                    print(f"File is not writable: {path}")
                    with open(config.log_path, "a") as f:
                        f.write(f"File is not writable: {path}\n")
            except PermissionError:
                print("Permission denied while deleting backup file.")
                with open(config.log_path, "a") as f:
                    f.write("Permission denied while deleting backup file.\n")
            except OSError as e:
                print(f"Error while deleting backup file: {e}")
                with open(config.log_path, "a") as f:
                    f.write(f"Error while deleting backup file: {e}\n")
            except Exception as e:
                print(f"Error while deleting backup file: {e}")
                with open(config.log_path, "a") as f:
                    f.write(f"Error while deleting backup file: {e}\n")


if __name__ == "__main__":
    config_path = config.essay_db_path
    delete_db(config_path, True)
