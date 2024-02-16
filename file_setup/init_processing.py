# file_setup\init_processing.py
"""
This file contains functions for processing files.

Functions include:

    - create_database(db_path: str) - Creates a database connection and a cursor to the specified database path.
    - open_database(db_path: str) - Opens a database connection and a cursor to the specified database path.
    - setup_lemmatizer() - Sets up the lemmatizer and stop words.
    - process_content(content: str, lemmatizer: Any, stop_words: set[str]) - Processes the specified content using the specified lemmatizer and stop words.
    - return_title_and_year(filename: str, filepath: str) - Returns the title and year of the specified file.
    - read_file_content(essay_dir: str) - Reads the content of all .odt and .docx files in the specified directory.
    - insert_into_database(db_path: str, table_name: str, column_name: str, data: Any) - Inserts data into the specified table in the database.
    - close_database(conn: sqlite3.Connection) - Closes a database connection.
    - main() - Main function to initialize the processing of the data.
"""

import os
import sqlite3
import time
import docx
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from odf import teletype, text as odf_text
from odf.opendocument import load

from file_setup.config import essay_db_path, dataset_dir


def create_database(db_path: str) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    """
    Creates a database connection and a cursor to the specified database path.

    Parameters:
        - db_path (str): The path to the database.

    Returns:
        - conn (sqlite3 Connection): The database connection.
        - cursor (sqlite3 Cursor): The database cursor.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create a table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS essays (
            id INTEGER PRIMARY KEY,
            title TEXT,
            year INTEGER,
            content TEXT
        )
    ''')
    conn.commit()
    return conn, cursor


def open_database(db_path: str) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    """
    Open a database connection using the provided database path.
    
    Parameters:
        - db_path: A string representing the path to the database file.
    
    Returns:
        - A tuple containing the connection and cursor objects.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn, cursor


def setup_lemmatizer() -> tuple[WordNetLemmatizer, set[str]]:
    """
    Set up the lemmatizer by downloading necessary NLTK resources and initializing 
    the lemmatizer, stop words, and essay directory.

    Parameters:
        - None

    Returns:
        - lemmatizer: the initialized WordNetLemmatizer
        - stop_words: a set of English stop words
    """
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')

    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    return lemmatizer, stop_words


def process_content(content: str, lemmatizer: WordNetLemmatizer, stop_words: set[str]) -> str:
    """
        Process the content by tokenizing, converting to lowercase, lemmatizing, and removing stop words.

        Parameters:
            - content (str): The input content to be processed.
            - lemmatizer: The lemmatizer object.
            - stop_words: A set of English stop words.

        Returns:
            - str: The processed content.
        """
    words = word_tokenize(content)
    words = [word.lower() for word in words if word.isalpha()]
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    processed_content = " ".join(words)
    return processed_content


def return_title_and_year(file_name: str, file_path: str) -> tuple[str, int]:
    """
    Returns the title and year of the given file.

    Parameters:
        - file_name (str): The name of the file.
        - file_path (str): The path to the file.

    Returns:
        - tuple[str, int]: A tuple containing the title of the file and the year of last modification.
    """
    title: str = os.path.splitext(file_name)[0].replace('_', ' ')
    last_modified_time: float = os.path.getmtime(file_path)
    year: int = time.gmtime(last_modified_time).tm_year

    return title, year


def read_file_content(essay_dir: str) -> list[tuple[str, int, str]]:
    """
    Reads the content of all .odt and .docx files in the specified directory.

    Parameters:
        - essay_dir (str): The directory containing the essays.

    Returns:
        - list[tuple[str, int, str]]: A list of tuples, each containing the title, year, and content of the file.
    """
    file_contents: list[tuple[str, int, str]] = []

    for filename in os.listdir(essay_dir):
        if filename.endswith('.odt') or filename.endswith('.docx'):
            filepath = os.path.join(essay_dir, filename)

            title, year = return_title_and_year(filename, filepath)

            content = ""
            if filename.endswith('.odt'):
                odt_file = load(filepath)
                all_text = odt_file.getElementsByType(odf_text.P)
                content = " ".join([teletype.extractText(text) for text in all_text])
            elif filename.endswith('.docx'):
                doc = docx.Document(filepath)
                content = " ".join([para.text for para in doc.paragraphs])

            file_contents.append((title, year, content))

    return file_contents


def insert_into_database(data: list[tuple[str, int, str]], conn: sqlite3.Connection, cursor: sqlite3.Cursor,
                         table_name: str, print_output: bool = False) -> None:
    """
    Insert data into the specified table in the database.

    Parameters:
        - data (list[tuple[str, int, str]]): A list of tuples containing the title, year, and processed content.
        - conn: The database connection object.
        - cursor: The database cursor object.
        - table_name (str): The name of the table to insert data into.
        - print_output (bool): Whether to print the processed content. Default is False.

    Returns:
        - None
    """
    try:
        for title, year, processed_content in data:
            if print_output:
                print(f"Title: {title}")
                print(f"Year: {year}")
                print(f"Processed Content: {processed_content[:100]}...")  # Print first 100 characters
                print("-----------------------------------")

            try:
                cursor.execute(f'INSERT INTO {table_name} (title, year, content) VALUES (?, ?, ?)',
                               (title, year, processed_content))
            except sqlite3.Error as e:
                print(f"An error occurred while inserting data: {e}")

            conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")


def close_database(conn: sqlite3.Connection) -> None:
    """
    Closes the database connection.
    
    Parameters:
        - conn: The database connection object.
    """
    if conn:
        conn.commit()
        conn.close()
        print("Database connection closed.")
    else:
        print("No database connection to close.")


def main():
    """
    Main function to initialize the processing of the data.
    Creates the database if it doesn't exist, otherwise opens it.
    Then processes the data files in the 'Test' directory and inserts them into the database.
    Closes the database connection.

    Parameters:
        - None

    Returns:
        - None
    """

    print("Initializing test data...")

    if not os.path.exists(essay_db_path):
        print("Database directory not found. Creating new database...")
        conn, cursor = create_database(essay_db_path)
    else:
        print("Database directory found. Using existing database...")
        conn, cursor = open_database(essay_db_path)

    lemmatizer, stop_words = setup_lemmatizer()

    file_contents = read_file_content(dataset_dir)
    processed_data = [(title, year, process_content(content, lemmatizer, stop_words)) for title, year, content in
                      file_contents]
    insert_into_database(processed_data, conn, cursor, 'essays', print_output=True)

    close_database(conn)
    print("Data initialization complete.")


if __name__ == '__main__':
    main()
