# tests/test_preprocessing.py

import unittest
from unittest.mock import patch, MagicMock

from file_setup.init_processing import *
from file_setup.config import test_db_path, test_dir, dataset_dir

class TestPreprocessing(unittest.TestCase):
    
    def test_setup_lemmatizer(self) -> None:
        lemmatizer, stop_words = setup_lemmatizer()
        self.assertIsInstance(lemmatizer, WordNetLemmatizer)
        self.assertIsInstance(stop_words, set)
    
    def test_process_content(self) -> None:
        
        lemmatizer, stop_words = setup_lemmatizer()
        content = "This is a test. Testing, 1, 2, 3!"
        expected_content = "test testing"
        
        processed_content = process_content(content, lemmatizer, stop_words)
        self.assertEqual(processed_content, expected_content)
    
    def test_create_database(self) -> None:
        test_db_path = os.path.join(test_dir, 'test.db')
        
        conn, cursor = create_database(test_db_path)
        
        self.assertIsNotNone(conn)
        self.assertIsInstance(conn, sqlite3.Connection)
        self.assertIsNotNone(cursor)
        self.assertIsInstance(cursor, sqlite3.Cursor)
        
        conn.close()
        
    def test_open_database(self) -> None:
        test_db_path = os.path.join(test_dir, 'test.db')
        
        conn, cursor = open_database(test_db_path)
        
        self.assertIsNotNone(conn)
        self.assertIsInstance(conn, sqlite3.Connection)
        self.assertIsNotNone(cursor)
        self.assertIsInstance(cursor, sqlite3.Cursor)
        
        conn.close()
    
    def test_close_database(self) -> None:
        test_db_path = os.path.join(test_dir, 'test.db')
        
        conn, cursor = open_database(test_db_path)
        
        self.assertIsNotNone(conn)
        self.assertIsInstance(conn, sqlite3.Connection)
        self.assertIsNotNone(cursor)
        self.assertIsInstance(cursor, sqlite3.Cursor)
        
        close_database(conn)
        
        with self.assertRaises(sqlite3.ProgrammingError):
            cursor.execute("SELECT 1")
        
    @patch('file_setup.init_processing.load')
    @patch('file_setup.init_processing.docx.Document')
    @patch('file_setup.init_processing.os.listdir')
    @patch('file_setup.init_processing.sqlite3.connect')
    @patch('file_setup.init_processing.time.gmtime')
    @patch('file_setup.init_processing.os.path.getmtime')
    @patch('file_setup.init_processing.process_content')
    def test_process_files(self, mock_process_content: MagicMock, mock_getmtime: MagicMock, mock_gmtime: MagicMock, mock_connect: MagicMock, mock_listdir: MagicMock, mock_docx: MagicMock, mock_load: MagicMock) -> None:
        # Arrange
        mock_getmtime.return_value = 1234567890
        mock_gmtime.return_value = time.struct_time((2020, 1, 1, 0, 0, 0, 0, 0, 0))
        mock_listdir.return_value = ['test.odt', 'test.docx']
        mock_load.return_value = MagicMock()
        mock_docx.return_value = MagicMock()
        mock_cursor = mock_connect.return_value.cursor.return_value
        
        lemmatizer = MagicMock()
        stop_words = set()
        essay_dir = 'dummy_dir'
        
        # Act
        process_files(essay_dir, lemmatizer, stop_words, mock_connect.return_value, mock_cursor)
        
        # Assert
        mock_load.assert_called_with(os.path.join(essay_dir, 'test.odt'))
        mock_docx.assert_called_with(os.path.join(essay_dir, 'test.docx'))
        mock_getmtime.assert_any_call(os.path.join(essay_dir, 'test.odt'))
        mock_getmtime.assert_any_call(os.path.join(essay_dir, 'test.docx'))
        mock_gmtime.assert_called_with(1234567890)
        self.assertTrue(mock_process_content.called)
        self.assertTrue(mock_cursor.execute.called)
        mock_connect.return_value.commit.assert_called()
    
    @patch('file_setup.init_processing.process_files')
    @patch('file_setup.init_processing.setup_lemmatizer')
    @patch('file_setup.init_processing.open_database')
    @patch('file_setup.init_processing.create_database')
    @patch('file_setup.init_processing.os.path.exists')
    @patch('file_setup.init_processing.close_database')
    def test_main(self, mock_close_db: MagicMock, mock_exists: MagicMock, mock_create_db: MagicMock, mock_open_db: MagicMock, mock_setup_lemmatizer: MagicMock, mock_process_files: MagicMock) -> None:
        # Arrange
        mock_exists.return_value = False
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_create_db.return_value = (mock_conn, mock_cursor)
        mock_lemmatizer = MagicMock()
        mock_stop_words = set()
        mock_setup_lemmatizer.return_value = (mock_lemmatizer, mock_stop_words)

        # Act
        main()

        # Assert
        mock_create_db.assert_called()
        mock_process_files.assert_called_with(dataset_dir, mock_lemmatizer, mock_stop_words, mock_conn, mock_cursor, print_output = True)
        mock_close_db.assert_called_with(mock_conn)
        
        mock_exists.return_value = True
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_open_db.return_value = (mock_conn, mock_cursor)
        main()
        
        mock_open_db.assert_called()
        mock_process_files.assert_called_with(dataset_dir, mock_lemmatizer, mock_stop_words, mock_conn, mock_cursor, print_output = True)
        mock_close_db.assert_called_with(mock_conn)


if __name__ == '__main__':
    unittest.main()
    
    os.remove(test_db_path)