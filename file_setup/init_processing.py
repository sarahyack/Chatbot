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

def create_database(db_path):
    """
    Creates a database connection and a cursor to the specified database path.

    Args:
        db_path (str): The path to the database.

    Returns:
        conn (sqlite3 Connection): The database connection.
        cursor (sqlite3 Cursor): The database cursor.
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

def open_database(db_path):
    """
    Open a database connection using the provided database path.

    :param db_path: A string representing the path to the database file.
    :return: A tuple containing the connection and cursor objects.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn, cursor

def setup_lemmatizer(data_dir):
    """
    Set up the lemmatizer by downloading necessary NLTK resources and initializing 
    the lemmatizer, stop words, and essay directory.

    Parameters:
    - data_dir: the directory where the data is located

    Returns:
    - lemmatizer: the initialized WordNetLemmatizer
    - stop_words: a set of English stop words
    - essay_dir: the directory path for the 'Test' data
    """
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')

    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    essay_dir = os.path.join(data_dir, 'Test')
    
    return lemmatizer, stop_words, essay_dir

def process_content(content, lemmatizer, stop_words):
        """
        Process the content by tokenizing, lowercasing, lemmatizing, and removing stop words.

        Parameters:
            content (str): The input content to be processed.

        Returns:
            str: The processed content.
        """
        words = word_tokenize(content)
        words = [word.lower() for word in words if word.isalpha()]
        words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
        processed_content = " ".join(words)
        return processed_content


def process_files(essay_dir, lemmatizer, stop_words, conn, cursor):
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
                
                try:
                    cursor.execute('INSERT INTO essays (title, content, year) VALUES (?, ?, ?)', (title, processed_content, year))
                except sqlite3.Error as e:
                    print(f"An error occurred while inserting data: {e}")
                
                conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        
def close_database(conn):
    """
    Closes the database connection.
    
    Parameters:
    - conn: The database connection object.
    """
    if conn:
        conn.commit()
        conn.close()

def main():
    from file_setup.config import database_dir, data_dir
    print("Initializing test data...")
    
    if not os.path.exists(database_dir):
        print("Database directory not found. Creating new database...")
        conn, cursor = create_database(database_dir)
    else:
        print("Database directory found. Using existing database...")
        conn, cursor = open_database(database_dir)
    lemmatizer, stop_words, essay_dir = setup_lemmatizer(data_dir)
    
    process_files(essay_dir, lemmatizer, stop_words, conn, cursor)
    
    close_database(conn)
    print("Data initialization complete.")

if __name__ == '__main__':
    main()