# tests/test_preprocessing.py

import unittest
from unittest.mock import patch, MagicMock
from typing import cast

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
        test_db_path_local: str = os.path.join(test_dir, 'test.db')

        conn, cursor = create_database(test_db_path)

        self.assertIsNotNone(conn)
        self.assertIsInstance(conn, sqlite3.Connection)
        self.assertIsNotNone(cursor)
        self.assertIsInstance(cursor, sqlite3.Cursor)

        conn.close()

    def test_open_database(self) -> None:
        test_db_path_local = os.path.join(test_dir, 'test.db')

        conn, cursor = open_database(test_db_path_local)

        self.assertIsNotNone(conn)
        self.assertIsInstance(conn, sqlite3.Connection)
        self.assertIsNotNone(cursor)
        self.assertIsInstance(cursor, sqlite3.Cursor)

        conn.close()

    def test_close_database(self) -> None:
        test_db_path_local = os.path.join(test_dir, 'test.db')

        conn, cursor = open_database(test_db_path_local)

        self.assertIsNotNone(conn)
        self.assertIsInstance(conn, sqlite3.Connection)
        self.assertIsNotNone(cursor)
        self.assertIsInstance(cursor, sqlite3.Cursor)

        close_database(conn)

        with self.assertRaises(sqlite3.ProgrammingError):
            cursor.execute("SELECT 1")

    @patch('file_setup.init_processing.os.path.getmtime')
    @patch('file_setup.init_processing.time.gmtime')
    @patch('file_setup.init_processing.os.path.splitext')
    def test_return_title_and_year(self, mock_splitext: MagicMock, mock_gmtime: MagicMock,
                                   mock_getmtime: MagicMock) -> None:
        mock_splitext.return_value = ('test_file', '.ext')
        mock_getmtime.return_value = 1234567890.0
        mock_gmtime.return_value = time.struct_time((2020, 1, 1, 0, 0, 0, 0, 0, 0))

        title, year = return_title_and_year('test_file.ext', '/path/to/test_file.ext')

        self.assertEqual(title, 'test file')
        self.assertEqual(year, 2020)

    @patch('file_setup.init_processing.return_title_and_year')
    @patch('file_setup.init_processing.os.listdir')
    @patch('file_setup.init_processing.os.path.join')
    @patch('file_setup.init_processing.load')
    @patch('file_setup.init_processing.docx.Document')
    def test_read_file_content(self, mock_docx: MagicMock, mock_load: MagicMock, mock_join: MagicMock,
                               mock_listdir: MagicMock, mock_return_title_and_year: MagicMock) -> None:
        mock_listdir.return_value = ['test_file.odt', 'test_file.docx']
        mock_join.side_effect = lambda a, b: f"{a}/{b}"
        mock_return_title_and_year.return_value = ('test file', 2020)

        mock_load.return_value = MagicMock()
        mock_docx.return_value = MagicMock()

        file_contents = read_file_content('/path/to/essays')

        self.assertEqual(len(file_contents), 2)

    @patch('file_setup.init_processing.sqlite3.Connection')
    @patch('file_setup.init_processing.sqlite3.Cursor')
    def test_insert_into_database(self, mock_cursor: MagicMock, mock_connection: MagicMock) -> None:
        mock_conn = mock_connection.return_value
        mock_cur = mock_cursor.return_value

        data = [(
            cast(str, 'test file'),
            cast(int, 2020),
            cast(str, 'processed content')
        )]
        insert_into_database(data, mock_conn, mock_cur, 'essays')

        # noinspection PyTypeChecker
        mock_cur.execute.assert_called_with('INSERT INTO essays (title, year, content) VALUES (?, ?, ?)', data[0])
        mock_conn.commit.assert_called()

    @patch('file_setup.init_processing.insert_into_database')
    @patch('file_setup.init_processing.process_content')
    @patch('file_setup.init_processing.read_file_content')
    @patch('file_setup.init_processing.setup_lemmatizer')
    @patch('file_setup.init_processing.open_database')
    @patch('file_setup.init_processing.create_database')
    @patch('file_setup.init_processing.os.path.exists')
    @patch('file_setup.init_processing.close_database')
    def test_main(self, mock_close_db: MagicMock, mock_exists: MagicMock, mock_create_db: MagicMock,
                  mock_open_db: MagicMock, mock_setup_lemmatizer: MagicMock, mock_read_file_content: MagicMock,
                  mock_process_content: MagicMock, mock_insert_into_database: MagicMock) -> None:
        # Arrange
        mock_exists.return_value = False
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_create_db.return_value = (mock_conn, mock_cursor)
        mock_lemmatizer = MagicMock()
        mock_stop_words = set()
        mock_setup_lemmatizer.return_value = (mock_lemmatizer, mock_stop_words)
        mock_read_file_content.return_value = [('test file', 2020, 'content')]

        mock_process_content.side_effect = lambda content, lemmatizer, stop_words: 'processed content'

        # Act
        main()

        # Assert
        mock_create_db.assert_called()
        mock_read_file_content.assert_called_with(dataset_dir)
        mock_process_content.assert_called_with('content', mock_lemmatizer, mock_stop_words)
        mock_insert_into_database.assert_called_with([('test file', 2020, 'processed content')], mock_conn, mock_cursor,
                                                     'essays', print_output=True)
        mock_close_db.assert_called_with(mock_conn)

        mock_exists.return_value = True
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_open_db.return_value = (mock_conn, mock_cursor)
        main()

        mock_open_db.assert_called()
        mock_read_file_content.assert_called_with(dataset_dir)
        mock_process_content.assert_called_with('content', mock_lemmatizer, mock_stop_words)
        mock_insert_into_database.assert_called_with([('test file', 2020, 'processed content')], mock_conn, mock_cursor,
                                                     'essays', print_output=True)
        mock_close_db.assert_called_with(mock_conn)


if __name__ == '__main__':
    unittest.main()

    os.remove(test_db_path)
