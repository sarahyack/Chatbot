# data/data_maintenance/restore.py

import shutil
import os
import file_setup.config as config


def restore_database(backup_file_path, db_path, delete_backup=False):
    if not os.path.exists(backup_file_path) or not os.path.isfile(backup_file_path):
        print("Backup file does not exist.")
        with open(config.log_path, "a") as f:
            f.write("Backup file does not exist.\n")
        raise FileNotFoundError("Backup file does not exist.")

    # Copy the backup file to the original database path
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
    backup_path = os.path.join(config.backup_dir, "your_backup_file.db")  # ""path/to/your/backup/file.db""
    restore_database(backup_path, database_path, delete_backup=False)
