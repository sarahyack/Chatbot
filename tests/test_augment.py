# tests/test_augment.py

import unittest
from unittest.mock import patch, MagicMock

from data.data_augmentation import augment
from data.data_augmentation.augment import main as augment_main


class TestAugment(unittest.TestCase):
    @patch('data.data_augmentation.augment.init_processing.main')
    @patch('data.data_augmentation.augment.data_query.column_exists')
    @patch('data.data_augmentation.augment.data_query.add_database_column')
    @patch('data.data_augmentation.augment.read_file_content')
    @patch('data.data_augmentation.augment.data_query.retrieve_id_from_database')
    @patch('data.data_augmentation.augment.data_query.update_database_cell')
    @patch('data.data_augmentation.augment.open_database')
    @patch('data.data_augmentation.augment.close_database')
    @patch('data.data_augmentation.augment.data_generation.summarize')
    @patch('data.data_augmentation.augment.data_generation.extract_entities')
    @patch('data.data_augmentation.augment.data_query.retrieve_table_data')
    @patch('data.data_augmentation.augment.data_query.is_column_empty_or_null')
    def test_augment_main(
        self,
        mock_is_column_empty_or_null: MagicMock,
        mock_retrieve_table_data: MagicMock,
        mock_extract_entities: MagicMock,
        mock_summarize: MagicMock,
        mock_close_database: MagicMock,
        mock_open_database: MagicMock,
        mock_update_database_cell: MagicMock,
        mock_retrieve_id_from_database: MagicMock,
        mock_read_file_content: MagicMock,
        mock_add_database_column: MagicMock,
        mock_column_exists: MagicMock,
        mock_init_main: MagicMock,
    ) -> None:

        mock_init_main.return_value = None
        mock_column_exists.return_value = False
        mock_is_column_empty_or_null.return_value = True
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_read_file_content.return_value = [('Test Title', 2020, 'Test Content')]
        mock_retrieve_id_from_database.return_value = 1
        mock_summarize.return_value = 'Test Summary'
        mock_extract_entities.return_value = [('Python', 'Programming Language')]
        mock_open_database.return_value = (mock_conn, mock_cursor)
        mock_retrieve_table_data.return_value = [(1, 'Test Title', 2020, 'Test Content', 'Test Summary', 'Python (Programming Language)')]
        mock_cursor.fetchall.return_value = [(1, 'Test Title')]
        expected_path = augment.essay_db_path

        augment_main()

        mock_init_main.assert_called_once()

        mock_add_database_column.assert_any_call(expected_path, 'essays', 'full_text')
        mock_add_database_column.assert_any_call(expected_path, 'essays', 'summary')
        mock_add_database_column.assert_any_call(expected_path, 'essays', 'keywords')

        mock_read_file_content.assert_called_once()
        mock_retrieve_id_from_database.assert_called_with(expected_path, 'essays', 'title', 'Test Title')
        mock_update_database_cell.assert_any_call(expected_path, 'essays', 1, 'full_text', 'Test Content')
        mock_update_database_cell.assert_any_call(expected_path, 'essays', 1, 'summary', 'Test Summary')
        mock_update_database_cell.assert_any_call(expected_path, 'essays', 1, 'keywords', 'Python (Programming Language)')

        mock_open_database.assert_called_once_with(expected_path)
        mock_close_database.assert_called_once()


if __name__ == '__main__':
    unittest.main()
