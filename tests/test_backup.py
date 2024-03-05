import unittest
from unittest.mock import patch, MagicMock, mock_open, call

from data.data_maintenance.backup import backup_database
from data.data_maintenance.remove import delete_db
from data.data_maintenance.restore import restore_database
import file_setup.config as config


class TestBackup(unittest.TestCase):
    @patch('os.path.exists')
    @patch('os.path.isfile')
    @patch('os.makedirs')
    @patch('shutil.copy2')
    @patch('builtins.open', new_callable=mock_open, read_data="data")
    def test_backup_database(self, mock_local_open: MagicMock, mock_copy2: MagicMock, mock_makedirs: MagicMock,
                             mock_isfile: MagicMock, mock_exists: MagicMock) -> None:
        mock_exists.return_value = True
        mock_isfile.return_value = True

        # Call function
        backup_database(config.essay_db_path, config.backup_dir)

        # Asserts
        mock_copy2.assert_called()
        mock_isfile.assert_called_with(config.essay_db_path)
        mock_local_open.assert_called_with(config.log_path, "a")

    @patch('builtins.input', return_value='y')
    @patch('os.remove')
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="data")
    def test_delete_db_accept(self, mock_file_open, mock_exists, mock_isfile, mock_remove, mock_input):
        db_path = config.essay_db_path

        delete_db(db_path)

        mock_input.assert_called_once_with(
            "Database file already exists. Do you want to overwrite it? Action cannot be undone. (y/n): ")
        mock_remove.assert_called_once_with(db_path)
        mock_file_open.assert_called_with(config.log_path, "a")

    @patch('builtins.input', return_value='n')
    @patch('os.remove')
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="data")
    def test_delete_db_decline(self, mock_file_open, mock_exists, mock_isfile, mock_remove, mock_input):
        db_path = config.essay_db_path

        delete_db(db_path)

        mock_input.assert_called_once_with(
            "Database file already exists. Do you want to overwrite it? Action cannot be undone. (y/n): ")
        mock_remove.assert_not_called()
        mock_file_open.assert_called_with(config.log_path, "a")

    @patch('os.remove')
    @patch('shutil.copy2')
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="data")
    def test_restore_database(self, mock_file_open, mock_exists, mock_isfile, mock_copy, mock_remove):
        # Setup paths
        backup_file_path = "path/to/your/backup/file.db"
        db_path = config.essay_db_path

        # Execute the restore function
        restore_database(backup_file_path, db_path, delete_backup=True)

        # Assertions
        mock_exists.assert_called_once_with(backup_file_path)
        mock_isfile.assert_called_once_with(backup_file_path)
        mock_copy.assert_called_once_with(backup_file_path, db_path)
        mock_remove.assert_called_once_with(backup_file_path)
        mock_file_open.assert_called_with(config.log_path, "a")

    @patch('os.remove')
    @patch('shutil.copy2')
    @patch('os.path.isfile', return_value=True)
    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="data")
    def test_restore_database_no_backup_deletion(self, mock_file_open, mock_exists, mock_isfile, mock_copy,
                                                 mock_remove):
        # Setup paths
        backup_file_path = "path/to/your/backup/file.db"
        db_path = config.essay_db_path

        # Execute the restore function with delete_backup=False
        restore_database(backup_file_path, db_path, delete_backup=False)

        # Assertions
        mock_exists.assert_called_once_with(backup_file_path)
        mock_isfile.assert_called_once_with(backup_file_path)
        mock_copy.assert_called_once_with(backup_file_path, db_path)
        mock_remove.assert_not_called()
        mock_file_open.assert_called_with(config.log_path, "a")


if __name__ == '__main__':
    unittest.main()
