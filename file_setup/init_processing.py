# file_setup\init_processing.py

import os
import time
import sqlite3
import docx
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from odf import text, teletype
from odf.opendocument import load

from file_setup.config import database_path, dataset_dir

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
            content TEXT,
            year INTEGER
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
        Process the content by tokenizing, lowercasing, lemmatizing, and removing stop words.

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


def process_files(essay_dir: str, lemmatizer: WordNetLemmatizer, stop_words: set[str], conn: sqlite3.Connection, cursor: sqlite3.Cursor, print_output: bool=False) -> None:
    '''
    Processes the files in the 'Test' directory and inserts them into the database.
    
    Parameters:
        - essay_dir: the directory path for the data
        - lemmatizer: the initialized WordNetLemmatizer
        - stop_words: a set of English stop words
        - conn: the database connection
        - cursor: the database cursor
    
    Returns:
        - None
    '''
    try:
        for filename in os.listdir(essay_dir):
            if filename.endswith('.odt') or filename.endswith('.docx'):
                filepath = os.path.join(essay_dir, filename)
                
                title = os.path.splitext(filename)[0].replace('_', ' ')

                last_modified_time = os.path.getmtime(filepath)
                year = time.gmtime(last_modified_time).tm_year
                
                content = ""
                
                if filename.endswith('.odt'):
                    odt_file = load(filepath)
                    all_text = odt_file.getElementsByType(text.P)
                    content = " ".join([teletype.extractText(text) for text in all_text])
                elif filename.endswith('.docx'):
                    doc = docx.Document(filepath)
                    content = " ".join([para.text for para in doc.paragraphs])
                    
                processed_content = process_content(content, lemmatizer, stop_words)
                
                if print_output:
                    print(f"Title: {title}")
                    print(f"Year: {year}")
                    print(f"Processed Content: {processed_content[:100]}...")  # Print first 100 characters
                    print("-----------------------------------")
                
                try:
                    cursor.execute('INSERT INTO essays (title, content, year) VALUES (?, ?, ?)', (title, processed_content, year))
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
    '''
    Main function to initialize the processing of the data.
    Creates the database if it doesn't exist, otherwise opens it.
    Then processes the data files in the 'Test' directory and inserts them into the database.
    Closes the database connection.
    
    Parameters:
        - None
    
    Returns:
        - None
    '''
    
    print("Initializing test data...")
    
    if not os.path.exists(database_path):
        print("Database directory not found. Creating new database...")
        conn, cursor = create_database(database_path)
    else:
        print("Database directory found. Using existing database...")
        conn, cursor = open_database(database_path)
    lemmatizer, stop_words = setup_lemmatizer()
    
    process_files(dataset_dir, lemmatizer, stop_words, conn, cursor, print_output=True)
    
    close_database(conn)
    print("Data initialization complete.")

if __name__ == '__main__':
    main()