import unittest
from unittest.mock import patch, MagicMock, mock_open, call

from data.data_maintenance.backup import backup_database
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
    @patch('os.path.exists')
    @patch('os.path.isfile')
    @patch('shutil.copy2')
    @patch('os.remove')
    @patch('builtins.open', new_callable=mock_open, read_data="data")
    def test_restore_database_overwrite(self, mock_file_open: MagicMock, mock_remove: MagicMock, mock_copy: MagicMock,
                                        mock_isfile: MagicMock, mock_exists: MagicMock, mock_input: MagicMock) -> None:
        mock_exists.side_effect = [True, True]
        mock_isfile.side_effect = [True, True]

        backup_file_path = "path/to/your/backup/file.db"
        db_path = config.essay_db_path

        restore_database(backup_file_path, db_path, delete_existing_db=True, delete_backup=True)

        mock_exists.assert_has_calls([call(backup_file_path), call(db_path)])
        mock_isfile.assert_has_calls([call(backup_file_path), call(db_path)])
        mock_remove.assert_has_calls(
            [call(db_path), call(backup_file_path)])  # Check both db and backup file are removed
        mock_copy.assert_called_with(backup_file_path, db_path)
        mock_file_open.assert_called_with(config.log_path, "a")
        mock_input.assert_called_once_with("Database file already exists. Do you want to overwrite it? Action cannot be undone. (y/n): ")

    @patch('builtins.input', return_value='n')  # Simulate user input 'n'
    @patch('os.path.exists', return_value=True)
    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data="data")
    def test_restore_database_no_overwrite(self, mock_file_open: MagicMock, mock_isfile: MagicMock,
                                           mock_exists: MagicMock, mock_input: MagicMock) -> None:
        backup_file_path = "path/to/your/backup/file.db"
        db_path = config.essay_db_path

        # Call function expecting no overwrite
        restore_database(backup_file_path, db_path, delete_existing_db=True, delete_backup=False)

        # Asserts that copy and remove are not called since user chose not to overwrite
        mock_file_open.assert_called_with(config.log_path, "a")
        mock_input.assert_called_once_with("Database file already exists. Do you want to overwrite it? Action cannot be undone. (y/n): ")


if __name__ == '__main__':
    unittest.main()
