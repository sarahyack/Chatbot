import unittest
from unittest.mock import patch, MagicMock, mock_open

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

    @patch('os.path.exists')
    @patch('os.path.isfile')
    @patch('shutil.copy2')
    @patch('os.remove')
    @patch('builtins.open', new_callable=mock_open, read_data="data")
    def test_restore_database(self, mock_file: MagicMock, mock_remove: MagicMock, mock_copy: MagicMock,
                              mock_isfile: MagicMock, mock_exists: MagicMock) -> None:
        mock_exists.return_value = True
        mock_isfile.return_value = True

        # Call function
        restore_database("path/to/your/backup/file.db", config.essay_db_path, delete_backup=True)

        # Asserts
        mock_copy.assert_called()
        mock_remove.assert_called()
        mock_file.assert_called_with(config.log_path, "a")


if __name__ == '__main__':
    unittest.main()
