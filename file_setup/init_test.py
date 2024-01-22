import os
import time
import sqlite3
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from config import paths

# Connect to SQLite database (the file will be created if it doesn't exist)
conn = sqlite3.connect('essays.db')
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

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
essay_dir = 'path/to/your/essays'

for filename in os.listdir(essay_dir):
    if filename.endswith('.odt'):  # Change this to match your file extension
        filepath = os.path.join(essay_dir, filename)
        
        # Extract title from filename
        title = os.path.splitext(filename)[0].replace('_', ' ')

        # Extract year from file's last modified time
        last_modified_time = os.path.getmtime(filepath)
        year = time.gmtime(last_modified_time).tm_year
        
        # Read and process the content of the file
        # You might need to use a library like odfpy for .odt files
        with open(filepath, 'r') as file:
            text = file.read()
            words = word_tokenize(text)
            words = [lemmatizer.lemmatize(word.lower()) for word in words if word.isalpha() and word.lower() not in stop_words]
            processed_content = ' '.join(words)
            
            # Insert into the database
            cursor.execute('INSERT INTO essays (title, content, year) VALUES (?, ?, ?)', (title, processed_content, year))

conn.commit()

conn.close()