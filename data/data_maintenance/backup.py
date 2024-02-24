# data/data_maintenance/backup.py
"""
Backup the database file in the backup directory.

Functions:
    - backup_database(db_path: str, backup_dir: str)
"""

import shutil
import os
from datetime import datetime
import file_setup.config as config


def backup_database(db_path: str, backup_dir: str) -> None:
    """
    Create a backup of the database file in the backup directory.

    Parameters:
        - db_path (str): The path to the database file.
        - backup_dir (str): The path to the backup directory.

    Raises:
        FileNotFoundError: If the database file does not exist.
        FileNotFoundError: If the backup directory does not exist.
        PermissionError: If the backup directory is not writable.

    Returns:
        None
    """
    if not os.path.exists(db_path) or not os.path.isfile(db_path):
        print("Database file does not exist.")
        with open(config.log_path, "a") as f:
            f.write("Database file does not exist.\n")
        raise FileNotFoundError("Database file does not exist.")

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        with open(config.log_path, "a") as f:
            f.write(f"Backup directory created: {backup_dir}\n")

    try:
        timestamp: str = datetime.now().strftime("%Y%m%d%H%M%S")
        db_name: str = os.path.basename(db_path)
        backup_name: str = f"{db_name}_backup_{timestamp}.db"
        backup_path: str = os.path.join(backup_dir, backup_name)

        shutil.copy2(db_path, backup_path)
        print(f"Backup created at {backup_path}")
        with open(config.log_path, "a") as f:
            f.write(f"Backup created at {backup_path}\n")
    except FileNotFoundError:
        print("Backup directory does not exist.")
        with open(config.log_path, "a") as f:
            f.write("Backup directory does not exist.\n")
    except PermissionError:
        print("Permission denied while creating backup.")
        with open(config.log_path, "a") as f:
            f.write("Permission denied while creating backup.\n")
    except Exception as e:
        print(f"Error creating backup: {e}")
        with open(config.log_path, "a") as f:
            f.write(f"Error creating backup: {e}\n")


if __name__ == "__main__":
    database_path = config.essay_db_path
    backup_directory = config.backup_dir
    backup_database(database_path, backup_directory)
