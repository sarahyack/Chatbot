# tests/test_maintenance.py

import unittest
from unittest.mock import call, patch, MagicMock, mock_open

from data.data_maintenance import maintain
from file_setup.config import log_path, essay_health_path


class TestMaintenance(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data="data")
    @patch('builtins.print')
    def test_generate_health_report(self, mock_print, mock_file):
        db_path = "test_db"
        table_name = "test_table"
        duplicates = ["column1", "column2"]
        empty_or_null_columns = ["column3"]
        actions_taken = {"Action1": "Details1", "Action2": "Details2"}

        maintain.generate_health_report(db_path, table_name, duplicates, empty_or_null_columns, actions_taken)

        # Check if the report is printed and written to a file
        mock_print.assert_called()
        mock_file.assert_called_with(open(log_path or essay_health_path, 'w'))

    @patch('data.data_augmentation.data_query.delete_row_by_id')
    def test_resolve_duplicates(self, mock_delete):
        duplicates = {
            "duplicate_title1": [3, 1, 2],
            "duplicate_title2": [6, 4, 5]
        }

        maintain.resolve_duplicates("dummy_db", "dummy_table", duplicates)

        expected_calls = [
            call("dummy_db", "dummy_table", 3),
            call("dummy_db", "dummy_table", 5),
            call("dummy_db", "dummy_table", 2),
            call("dummy_db", "dummy_table", 6),
        ]
        mock_delete.assert_has_calls(expected_calls, any_order=True)

    @patch('data.data_augmentation.data_query.drop_database_column')
    @patch('data.data_augmentation.data_query.is_column_empty_or_null')
    @patch('data.data_augmentation.data_query.column_exists')
    @patch('data.data_augmentation.data_query.find_all_duplicates')
    @patch('data.data_maintenance.maintain.open_database')
    @patch('data.data_maintenance.maintain.close_database')
    @patch('data.data_maintenance.maintain.generate_health_report')
    def test_main(self, mock_generate_report, mock_close_db, mock_open_db, mock_find_duplicates, mock_column_exists,
                  mock_is_empty_or_null, mock_drop_column):
        # Mock the return values for database interactions
        mock_open_db.return_value = (MagicMock(), MagicMock())
        mock_column_exists.return_value = True
        mock_is_empty_or_null.return_value = False
        mock_find_duplicates.return_value = {}

        maintain.main()

        # Check if the necessary functions are called
        mock_open_db.assert_called()
        mock_close_db.assert_called()
        mock_generate_report.assert_called()


if __name__ == '__main__':
    unittest.main()
