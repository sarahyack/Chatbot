# data/data_maintenance/restore.py
"""
This module contains functions for data maintenance. remove.py must be run before restore.py.

Functions include:
    - restore_database(backup_file_path: str, db_path: str, delete_existing_db: bool = True, delete_backup: bool = False)
        Restore the database from a backup file.

"""

import shutil
import os
import file_setup.config as config


def restore_database(backup_file_path: str, db_path: str, delete_backup: bool = False) -> None:
    """
    Restore the database from a backup file.

    Parameters:
        - backup_file_path (str): The path to the backup file.
        - db_path (str): The path to the database file.
        - delete_existing_db (bool, optional): Whether to delete the existing database file. Defaults to True.
        - delete_backup (bool, optional): Whether to delete the backup file. Defaults to False.

    Raises:
        FileNotFoundError: If the backup file does not exist.
        FileNotFoundError: If the database file already exists and delete_existing_db is True.
        PermissionError: If the database file is not writable.

    Returns:
        None
    """
    if not os.path.exists(backup_file_path) or not os.path.isfile(backup_file_path):
        print("Backup file does not exist.")
        with open(config.log_path, "a") as f:
            f.write("Backup file does not exist.\n")
        raise FileNotFoundError("Backup file does not exist.")

    try:
        shutil.copy2(backup_file_path, db_path)
        print(f"Database restored from {backup_file_path} to {db_path}")
        with open(config.log_path, "a") as f:
            f.write(f"Database restored from {backup_file_path} to {db_path}\n")

        if delete_backup:
            os.remove(backup_file_path)
            print(f"Backup file deleted: {backup_file_path}")
            with open(config.log_path, "a") as f:
                f.write(f"Backup file deleted: {backup_file_path}\n")
    except PermissionError:
        print("Permission denied while restoring database.")
        with open(config.log_path, "a") as f:
            f.write("Permission denied while restoring database.\n")
    except FileNotFoundError:
        print("Database file does not exist.")
        with open(config.log_path, "a") as f:
            f.write("Database file does not exist.\n")
    except Exception as e:
        print(f"Error while restoring database: {e}")
        with open(config.log_path, "a") as f:
            f.write(f"Error while restoring database: {e}\n")


if __name__ == "__main__":
    database_path = config.essay_db_path
    backup_path = os.path.join(config.backup_dir, "essays.db_backup_20240220171652.db")  # ""file_name.db""
    restore_database(backup_path, database_path, delete_backup=False)
