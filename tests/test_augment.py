# tests/test_augment.py

import unittest
from unittest.mock import patch, MagicMock
from data.data_augmentation import augment as main_module


class TestDataAugment(unittest.TestCase):
    @patch('data.data_augmentation.augment.data_query.add_database_column')
    @patch('data.data_augmentation.augment.read_file_content')
    @patch('data.data_augmentation.augment.data_query.insert_into_database')
    @patch('data.data_augmentation.augment.open_database')
    @patch('data.data_augmentation.augment.data_query.update_database_cell')
    @patch('data.data_augmentation.augment.data_generation.summarize')
    @patch('data.data_augmentation.augment.data_generation.extract_entities')
    @patch('data.data_augmentation.augment.data_query.retrieve_table_data')
    @patch('data.data_augmentation.augment.data_query.column_exists')
    def test_main(self, mock_column_exists: MagicMock, mock_retrieve_table_data: MagicMock,
                  mock_extract_entities: MagicMock, mock_summarize: MagicMock, mock_update_database_cell: MagicMock,
                  mock_open_database: MagicMock, mock_insert_into_database: MagicMock,
                  mock_read_file_content: MagicMock, mock_add_database_column: MagicMock) -> None:
        pass
        # Set up mock return values
        mock_read_file_content.return_value = [('Test Title', 2020, 'Test Content')]
        mock_summarize.return_value = 'Test Summary'
        mock_extract_entities.return_value = [('Python', 'Programming Language')]
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_open_database.return_value = (mock_conn, mock_cursor)
        mock_cursor.fetchall.return_value = [(1, 'Test Content')]
        mock_column_exists.return_value = False

        # Run the main function
        main_module.main()

        # Assertions
        mock_add_database_column.assert_any_call(main_module.database_path, 'essays', 'full_text')
        mock_add_database_column.assert_any_call(main_module.database_path, 'essays', 'summary')
        mock_add_database_column.assert_any_call(main_module.database_path, 'essays', 'keywords')
        mock_read_file_content.assert_called_with(main_module.dataset_dir)
        mock_summarize.assert_called_with('Test Content', 5)
        mock_extract_entities.assert_called_with('Test Content')
        mock_update_database_cell.assert_any_call(main_module.database_path, 'essays', 1, 'summary', 'Test Summary')
        mock_update_database_cell.assert_any_call(main_module.database_path, 'essays', 1, 'keywords',
                                                  'Python (Programming Language)')


if __name__ == '__main__':
    unittest.main()
