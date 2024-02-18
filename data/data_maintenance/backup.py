# data/data_maintenance/backup.py

import shutil
import os
from datetime import datetime
import file_setup.config as config


def backup_database(db_path, backup_dir):
    if not os.path.exists(db_path) or not os.path.isfile(db_path):
        print("Database file does not exist.")
        with open(config.log_path, "a") as f:
            f.write("Database file does not exist.\n")
        raise FileNotFoundError("Database file does not exist.")

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        with open(config.log_path, "a") as f:
            f.write(f"Backup directory created: {backup_dir}\n")

    # Create a timestamped backup file name
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        db_name = os.path.basename(db_path)
        backup_name = f"{db_name}_backup_{timestamp}.db"
        backup_path = os.path.join(backup_dir, backup_name)

        # Copy the database file to the backup directory
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
