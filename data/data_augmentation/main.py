# data\data_augmentation\main.py

from data.data_augmentation import data_query, data_generation
from file_setup.init_processing import *
from file_setup.config import *

def main():
    print("Initializing test data...")
    if not data_query.column_exists(database_path, 'essays', 'full_text'):
        data_query.add_database_column(database_path, 'essays', 'full_text')
    if not data_query.column_exists(database_path, 'essays', 'summary'):
        data_query.add_database_column(database_path, 'essays', 'summary')
    if not data_query.column_exists(database_path, 'essays', 'keywords'):
        data_query.add_database_column(database_path, 'essays', 'keywords')
    
    if data_query.is_column_empty_or_null(database_path, 'essays', 'full_text'):
        print("Reading file content...")
        full_content = read_file_content(dataset_dir)
        
        print("Inserting data...")
        for title, year, content in full_content:
            essay_id = data_query.retrieve_id_from_database(database_path, 'essays', 'title', title)
            if essay_id is not None:
                data_query.update_database_cell(database_path, 'essays', essay_id, 'full_text', content)
            else:
                print(f"Skipping {title}...")
        
        print("Done updating database!")
    
    print("Generating data...")
    conn, cursor = open_database(database_path)
    cursor.execute("SELECT id, full_text FROM essays")
    
    for row in cursor.fetchall():
        essay_id, full_text = row
        summary: str = data_generation.summarize(full_text, 5)
        data_query.update_database_cell(database_path, 'essays', essay_id, 'summary', summary)
        keywords: str = ', '.join(['{} ({})'.format(entity, label) for entity, label in data_generation.extract_entities(full_text)])
        data_query.update_database_cell(database_path, 'essays', essay_id, 'keywords', keywords)
    
    print("Done!")
    
    print(data_query.retrieve_table_data(database_path, 'essays'))
    print("Closing database...")
    close_database(conn)


if __name__ == '__main__':
    main()