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
    def test_column_exists(self, mock_sqlite3: MagicMock, mock_close_db: MagicMock, mock_open_db: MagicMock) -> None:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_sqlite3.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_open_db.return_value = (mock_conn, mock_cursor)

        mock_cursor.fetchall.return_value = [
            (0, 'id', 'int', 0, None, 0),
            (1, 'title', 'text', 0, None, 0),
            (2, 'full_text', 'text', 0, None, 0)
        ]

        mock_cursor.execute.return_value = None

        result = data_query.column_exists('dummy_path', 'dummy_table', 'full_text')

        self.assertTrue(result)

        mock_cursor.fetchall.return_value = [
            (0, 'id', 'int', 0, None, 0),
            (1, 'title', 'text', 0, None, 0)
        ]

        result = data_query.column_exists('dummy_path', 'dummy_table', 'full_text')

        self.assertFalse(result)

    @patch('file_setup.init_processing.open_database')
    @patch('file_setup.init_processing.close_database')
    @patch('file_setup.init_processing.sqlite3')
    def test_is_column_empty_or_null(self, mock_sqlite3, mock_close_db, mock_open_db):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_sqlite3.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_open_db.return_value = (mock_conn, mock_cursor)

        # Test case where the column has empty or null values
        mock_cursor.fetchone.return_value = (1,)  # Indicates 1 row with empty or null value
        result = data_query.is_column_empty_or_null('dummy_path', 'dummy_table', 'dummy_column')
        self.assertTrue(result)
        mock_cursor.execute.assert_called_with(
            "SELECT COUNT(*) FROM dummy_table WHERE dummy_column IS NULL OR dummy_column = ''")

        # Test case where the column does not have empty or null values
        mock_cursor.fetchone.return_value = (0,)  # Indicates no rows with empty or null value
        result = data_query.is_column_empty_or_null('dummy_path', 'dummy_table', 'dummy_column')
        self.assertFalse(result)
        mock_cursor.execute.assert_called_with(
            "SELECT COUNT(*) FROM dummy_table WHERE dummy_column IS NULL OR dummy_column = ''")

    @patch('file_setup.init_processing.open_database')
    @patch('file_setup.init_processing.close_database')
    @patch('file_setup.init_processing.sqlite3')
    def test_find_all_duplicates(self, mock_sqlite3, mock_close_db, mock_open_db):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            ('duplicate_title_1', 'duplicate_year_1', 2, '2,5'),
            ('duplicate_title_2', 'duplicate_year_2', 3, '3,6,8')
        ]
        mock_sqlite3.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_open_db.return_value = (mock_conn, mock_cursor)

        duplicates = data_query.find_all_duplicates('dummy_path', 'dummy_table', ['title', 'year'])

        expected_result = {
            ('duplicate_title_1', 'duplicate_year_1'): [2, 5],
            ('duplicate_title_2', 'duplicate_year_2'): [3, 6, 8]
        }
        self.assertEqual(duplicates, expected_result)
        mock_cursor.execute.assert_called_with(
            "SELECT title, year, COUNT(*), GROUP_CONCAT(id) FROM dummy_table GROUP BY title, year HAVING COUNT(*) > 1"
        )

    @patch('file_setup.init_processing.open_database')
    @patch('file_setup.init_processing.close_database')
    @patch('file_setup.init_processing.sqlite3')
    def test_add_database_column(self, mock_sqlite3: MagicMock, mock_close_db: MagicMock, mock_open_db: MagicMock) -> None:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_sqlite3.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_open_db.return_value = (mock_conn, mock_cursor)

        data_query.add_database_column('dummy_path', 'dummy_table', 'new_column')

        mock_cursor.execute.assert_called_with("ALTER TABLE dummy_table ADD COLUMN new_column TEXT")

    @patch('file_setup.init_processing.open_database')
    @patch('file_setup.init_processing.close_database')
    @patch('file_setup.init_processing.sqlite3')
    def test_drop_database_column(self, mock_sqlite3: MagicMock, mock_close_db: MagicMock,
                                  mock_open_db: MagicMock) -> None:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_sqlite3.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_open_db.return_value = (mock_conn, mock_cursor)

        data_query.drop_database_column('dummy_path', 'dummy_table', 'dummy_column')

        mock_cursor.execute.assert_called_with("ALTER TABLE dummy_table DROP COLUMN dummy_column")

    @patch('file_setup.init_processing.open_database')
    @patch('file_setup.init_processing.close_database')
    @patch('file_setup.init_processing.sqlite3')
    def test_delete_row_by_id(self, mock_sqlite3, mock_close_db, mock_open_db):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_sqlite3.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_open_db.return_value = (mock_conn, mock_cursor)
        dummy_id = 42

        data_query.delete_row_by_id('dummy_path', 'dummy_table', dummy_id)

        mock_cursor.execute.assert_called_with("DELETE FROM dummy_table WHERE id = ?", (dummy_id,))
        mock_conn.commit.assert_called()

    @patch('file_setup.init_processing.open_database')
    @patch('file_setup.init_processing.close_database')
    @patch('file_setup.init_processing.sqlite3')
    def test_update_database_column(self, mock_sqlite3: MagicMock, mock_close_db: MagicMock,
                                    mock_open_db: MagicMock) -> None:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_sqlite3.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_open_db.return_value = (mock_conn, mock_cursor)

        data_query.update_database_column('dummy_path', 'dummy_table', 'dummy_column', 'dummy_value')

        mock_cursor.execute.assert_called_with("UPDATE dummy_table SET dummy_column = 'dummy_value'")

    @patch('file_setup.init_processing.open_database')
    @patch('file_setup.init_processing.close_database')
    @patch('file_setup.init_processing.sqlite3')
    def test_update_database_cell(self, mock_sqlite3: MagicMock, mock_close_db: MagicMock,
                                  mock_open_db: MagicMock) -> None:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_sqlite3.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_open_db.return_value = (mock_conn, mock_cursor)
        dummy_id = 1

        data_query.update_database_cell('dummy_path', 'dummy_table', dummy_id, 'dummy_column', 'dummy_value')

        mock_cursor.execute.assert_called_with("UPDATE dummy_table SET dummy_column = ? WHERE id = ?",
                                               ('dummy_value', dummy_id))

    @patch('file_setup.init_processing.open_database')
    @patch('file_setup.init_processing.close_database')
    @patch('file_setup.init_processing.sqlite3')
    def test_retrieve_id_from_database(self, mock_sqlite3: MagicMock, mock_close_db: MagicMock,
                                       mock_open_db: MagicMock) -> None:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_sqlite3.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_open_db.return_value = (mock_conn, mock_cursor)
        dummy_value = 'dummy_value'

        dummy_value = 'dummy_value'
        mock_cursor.fetchone.return_value = (42,)
        dummy_id = data_query.retrieve_id_from_database('dummy_path', 'dummy_table', 'dummy_column', dummy_value)
        mock_cursor.execute.assert_called_with("SELECT id FROM dummy_table WHERE dummy_column = ?", (dummy_value,))
        self.assertEqual(dummy_id, 42)

        mock_cursor.fetchone.return_value = None
        dummy_id = data_query.retrieve_id_from_database('dummy_path', 'dummy_table', 'dummy_column', dummy_value)
        self.assertIsNone(dummy_id)

    @patch('file_setup.init_processing.open_database')
    @patch('file_setup.init_processing.close_database')
    @patch('file_setup.init_processing.sqlite3')
    def test_rename_database_column(self, mock_sqlite3: MagicMock, mock_close_db: MagicMock,
                                    mock_open_db: MagicMock) -> None:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_sqlite3.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_open_db.return_value = (mock_conn, mock_cursor)

        data_query.rename_database_column('dummy_path', 'dummy_table', 'dummy_old_column', 'dummy_new_column')

        mock_cursor.execute.assert_called_with(
            "ALTER TABLE dummy_table RENAME COLUMN dummy_old_column TO dummy_new_column")

    @patch('file_setup.init_processing.open_database')
    @patch('file_setup.init_processing.close_database')
    @patch('file_setup.init_processing.sqlite3')
    def test_insert_into_database(self, mock_sqlite3: MagicMock, mock_close_db: MagicMock,
                                  mock_open_db: MagicMock) -> None:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_sqlite3.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_open_db.return_value = (mock_conn, mock_cursor)

        dummy_columns = ['dummy_column']
        data_query.insert_into_database('dummy_path', 'dummy_table', dummy_columns, 'dummy_data')

        mock_cursor.executemany.assert_called_with("INSERT INTO dummy_table (dummy_column) VALUES (?)", ('dummy_data'))

    @patch('file_setup.init_processing.open_database')
    @patch('file_setup.init_processing.close_database')
    @patch('file_setup.init_processing.sqlite3')
    def test_retrieve_table_data(self, mock_sqlite3: MagicMock, mock_close_db: MagicMock,
                                 mock_open_db: MagicMock) -> None:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_sqlite3.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_cursor.fetchall.return_value = [('row1',), ('row2',)]
        mock_cursor.description = [('column1',)]
        mock_open_db.return_value = (mock_conn, mock_cursor)

        df = data_query.retrieve_table_data('dummy_path', 'dummy_table')

        self.assertEqual(len(df), 2)
        self.assertEqual(df.columns.tolist(), ['column1'])
        mock_cursor.execute.assert_called_with("SELECT * FROM dummy_table")

    @patch('file_setup.init_processing.open_database')
    @patch('file_setup.init_processing.close_database')
    @patch('file_setup.init_processing.sqlite3')
    def test_create_dataframe(self, mock_sqlite3: MagicMock, mock_close_db: MagicMock, mock_open_db: MagicMock) -> None:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_sqlite3.connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_open_db.return_value = (mock_conn, mock_cursor)

        data_query.create_dataframe('dummy_table')

        mock_cursor.execute.assert_called_with("SELECT * FROM dummy_table")


if __name__ == '__main__':
    unittest.main()

    if os.path.exists(test_db_path):
        os.remove(test_db_path)
