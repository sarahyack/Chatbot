# data\data_augmentation\main.py

from data.data_augmentation import data_query, data_generation
from file_setup.init_processing import *
from file_setup.config import *

print(data_query.retrieve_table_data(database_path, 'essays'))

def main():
    data_query.add_database_column(database_path, 'essays', 'full_text')
    data_query.add_database_column(database_path, 'essays', 'summary')
    data_query.add_database_column(database_path, 'essays', 'keywords')
    
    
    