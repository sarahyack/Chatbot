# tests/test_maintenance.py

import unittest
from unittest.mock import call, patch, MagicMock, mock_open, ANY

from data.data_maintenance import maintain
from file_setup.config import log_path, essay_db_path, test_db_path


class TestMaintenance(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data="data")
    @patch('builtins.print')
    def test_generate_health_report(self, mock_print, mock_file):
        db_path = "test_db"
        table_name = "test_table"
        duplicates = ["column1", "column2"]
        empty_or_null_columns = ["column3"]
        actions_taken = {"Action1": "Details1", "Action2": "Details2"}
        expected_path = log_path

        maintain.generate_health_report(db_path, table_name, duplicates, empty_or_null_columns, actions_taken)

        mock_print.assert_called()
        mock_file.assert_called_with(expected_path, 'a')

    @patch('data.data_augmentation.data_query.delete_row_by_id')
    def test_resolve_duplicates(self, mock_delete):
        duplicates = {
            ("duplicate_title1", "duplicate_year_1"): [1, 2, 3],
            ("duplicate_title1", "duplicate_year_2"): [4, 5, 6]
        }

        maintain.resolve_duplicates("dummy_db", "dummy_table", duplicates)

        expected_calls = [
            call("dummy_db", "dummy_table", 3),
            call("dummy_db", "dummy_table", 5),
            call("dummy_db", "dummy_table", 2),
            call("dummy_db", "dummy_table", 6),
        ]
        mock_delete.assert_has_calls(expected_calls, any_order=True)

    @patch('builtins.input', return_value='y')
    @patch('data.data_augmentation.data_query.drop_database_column')
    @patch('data.data_augmentation.data_query.is_column_empty_or_null')
    @patch('data.data_augmentation.data_query.column_exists')
    @patch('data.data_augmentation.data_query.find_all_duplicates')
    @patch('data.data_maintenance.maintain.open_database')
    @patch('data.data_maintenance.maintain.close_database')
    @patch('data.data_maintenance.maintain.generate_health_report')
    @patch('data.data_maintenance.maintain.resolve_duplicates')
    def test_main(self, mock_resolve_duplicates, mock_generate_report, mock_close_db, mock_open_db, mock_find_duplicates, mock_column_exists,
                  mock_is_empty_or_null, mock_drop_column, mock_input):
        mock_cursor = MagicMock()
        mock_cursor.execute.return_value.fetchall.return_value = [
            (1, 'title', 'TEXT', 0, None, 0),
            (2, 'year', 'INTEGER', 0, None, 0),
            # Add more columns as needed
        ]
        mock_conn = MagicMock()
        mock_open_db.return_value = (mock_conn, mock_cursor)
        mock_column_exists.return_value = True
        mock_is_empty_or_null.side_effect = [False, True]
        mock_find_duplicates.return_value = {
            ('title', 'year'): [2, 3, 5]
        }
        expected_path = essay_db_path
        expected_table_name = 'essays'

        maintain.main()

        mock_open_db.assert_called_once_with(expected_path)
        mock_close_db.assert_called_once_with(mock_conn)

        mock_find_duplicates.assert_called_with(expected_path, expected_table_name, ['title', 'year'])

        self.assertEqual(mock_is_empty_or_null.call_count, 2)

        mock_drop_column.assert_called_once()

        mock_resolve_duplicates.assert_called_with(expected_path, expected_table_name, {('title', 'year'): [2, 3, 5]})

        mock_generate_report.assert_called_once_with(expected_path, expected_table_name, {('title', 'year'): [2, 3, 5]},
                                                     ['year'], {'Remove empty or null column: year': f'ALTER TABLE {expected_table_name} DROP COLUMN year', 'Resolve duplicates': ANY})


if __name__ == '__main__':
    unittest.main()
