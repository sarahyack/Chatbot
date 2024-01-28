# tests/test_querying.py

import os
import unittest
from unittest.mock import patch, MagicMock

from data.data_augmentation import data_query
from file_setup.config import test_db_path


class TestDataQuery(unittest.TestCase):
    @patch('file_setup.init_processing.open_database')
    @patch('file_setup.init_processing.close_database')
    @patch('file_setup.init_processing.sqlite3')
    def test_add_database_column(self, mock_sqlite3: MagicMock, mock_close_db: MagicMock, mock_open_db: MagicMock) -> None:
        # Arrange
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_sqlite3.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_open_db.return_value = (mock_conn, mock_cursor)

        # Test function
        data_query.add_database_column('dummy_path', 'dummy_table', 'new_column')

        # Assert
        mock_cursor.execute.assert_called_with("ALTER TABLE dummy_table ADD COLUMN new_column TEXT")
    
    @patch('file_setup.init_processing.open_database')
    @patch('file_setup.init_processing.close_database')
    @patch('file_setup.init_processing.sqlite3')
    def test_drop_database_column(self, mock_sqlite3: MagicMock, mock_close_db: MagicMock, mock_open_db: MagicMock) -> None:
        # Arrange
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_sqlite3.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_open_db.return_value = (mock_conn, mock_cursor)

        # Test function
        data_query.drop_database_column('dummy_path', 'dummy_table', 'dummy_column')

        # Assert
        mock_cursor.execute.assert_called_with("ALTER TABLE dummy_table DROP COLUMN dummy_column")
    
    @patch('file_setup.init_processing.open_database')
    @patch('file_setup.init_processing.close_database')
    @patch('file_setup.init_processing.sqlite3')
    def test_create_dataframe(self, mock_sqlite3: MagicMock, mock_close_db: MagicMock, mock_open_db: MagicMock) -> None:
        # Arrange
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_sqlite3.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_open_db.return_value = (mock_conn, mock_cursor)

        # Test function
        data_query.create_dataframe('dummy_table')

        # Assert
        mock_cursor.execute.assert_called_with("SELECT * FROM dummy_table")
    
    @patch('file_setup.init_processing.open_database')
    @patch('file_setup.init_processing.close_database')
    @patch('file_setup.init_processing.sqlite3')
    def test_update_database_column(self, mock_sqlite3: MagicMock, mock_close_db: MagicMock, mock_open_db: MagicMock) -> None:
        # Arrange
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_sqlite3.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_open_db.return_value = (mock_conn, mock_cursor)

        # Test function
        data_query.update_database_column('dummy_path', 'dummy_table', 'dummy_column', 'dummy_value')

        # Assert
        mock_cursor.execute.assert_called_with("UPDATE dummy_table SET dummy_column = 'dummy_value'")

    @patch('file_setup.init_processing.open_database')
    @patch('file_setup.init_processing.close_database')
    @patch('file_setup.init_processing.sqlite3')
    def test_rename_database_column(self, mock_sqlite3: MagicMock, mock_close_db: MagicMock, mock_open_db: MagicMock) -> None:
        # Arrange
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_sqlite3.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_open_db.return_value = (mock_conn, mock_cursor)

        # Test function
        data_query.rename_database_column('dummy_path', 'dummy_table', 'dummy_old_column', 'dummy_new_column')

        # Assert
        mock_cursor.execute.assert_called_with("ALTER TABLE dummy_table RENAME COLUMN dummy_old_column TO dummy_new_column")
    
    @patch('file_setup.init_processing.open_database')
    @patch('file_setup.init_processing.close_database')
    @patch('file_setup.init_processing.sqlite3')
    def test_retrieve_table_data(self, mock_sqlite3: MagicMock, mock_close_db: MagicMock, mock_open_db: MagicMock) -> None:
        # Arrange
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_sqlite3.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        mock_cursor.fetchall.return_value = [('row1',), ('row2',)]
        mock_cursor.description = [('column1',)]
        mock_open_db.return_value = (mock_conn, mock_cursor)

        # Test function
        df = data_query.retrieve_table_data('dummy_path', 'dummy_table')

        # Assert
        self.assertEqual(len(df), 2)
        self.assertEqual(df.columns.tolist(), ['column1'])
        mock_cursor.execute.assert_called_with("SELECT * FROM dummy_table")

if __name__ == '__main__':
    unittest.main()
    
    if os.path.exists(test_db_path):
        os.remove(test_db_path)