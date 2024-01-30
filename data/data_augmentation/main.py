from data.data_augmentation import data_query, data_generation
from file_setup import init_processing
from file_setup import config

print(data_query.retrieve_table_data(config.database_path, 'essays'))