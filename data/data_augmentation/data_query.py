# data/data_augmentation/data_query.py
'''
This file contains functions for querying and manipulating data in a SQLite database.

Functions include:
    
    - add_database_column(db_path: str, table_name: str, column_name: str) - Add a new column to the specified table in the database.
    - drop_database_column(db_path: str, table_name: str, column_name: str) - Drops the specified column from the given database table.
    - rename_database_column(db_path: str, table_name: str, old_column_name: str, new_column_name: str) - Renames the specified column in the specified table in the database.
    - update_database_column(db_path: str, table_name: str, column_name: str, value: str) - Updates the value of the specified column in the specified table in the database.
    - insert_into_database(db_path: str, table_name: str, column_name: str, data: Any) - Insert data into the specified table in the database.
    - retrieve_table_data(db_path: str, table_name: str) - Retrieves the data from the specified table in the database.
    - create_dataframe(table_name: str) - Create a dataframe from the specified table and return it.
'''

from typing import Any
import pandas as pd
from file_setup import config
from file_setup.init_processing import open_database, close_database

def add_database_column(db_path: str, table_name: str, column_name: str) -> None:
    '''
    Add a new column to the specified table in the database.
    
    Parameters:
        - db_path (str): The path to the database file.
        - table_name (str): The name of the table to add the column to.
        - column_name (str): The name of the new column.
    
    Returns:
        - None
    '''
    conn, cursor = open_database(db_path)
    cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} TEXT")
    close_database(conn)
    
def drop_database_column(db_path: str, table_name: str, column_name: str) -> None:
    """
    Drops the specified column from the given database table.

    Parameters:
        - db_path (str): The path to the database.
        - table_name (str): The name of the table.
        - column_name (str): The name of the column to be dropped.

    Returns:
        None
    """
    conn, cursor = open_database(db_path)
    cursor.execute(f"ALTER TABLE {table_name} DROP COLUMN {column_name}")
    close_database(conn)

def update_database_column(db_path: str, table_name: str, column_name: str, value: str) -> None:
    '''
    Updates the value of the specified column in the specified table in the database.
    
    Parameters:
        - db_path (str): The path to the database file.
        - table_name (str): The name of the table to update.
        - column_name (str): The name of the column to update.
        - value (str): The new value for the column.
    
    Returns:
        - None
    '''
    conn, cursor = open_database(db_path)
    cursor.execute(f"UPDATE {table_name} SET {column_name} = '{value}'")
    close_database(conn)

def rename_database_column(db_path: str, table_name: str, old_column_name: str, new_column_name: str) -> None:
    '''
    Renames the specified column in the specified table in the database.
    
    Parameters:
        - db_path (str): The path to the database file.
        - table_name (str): The name of the table to rename the column in.
        - old_column_name (str): The name of the column to be renamed.
        - new_column_name (str): The new name for the column.
    
    Returns:
        - None
    '''
    conn, cursor = open_database(db_path)
    cursor.execute(f"ALTER TABLE {table_name} RENAME COLUMN {old_column_name} TO {new_column_name}")
    close_database(conn)

def insert_into_database(db_path: str, table_name: str, column_name: str, data: Any) -> None:
    '''
    Insert data into the specified table in the database.
    
    Parameters:
        - db_path (str): The path to the database file.
        - table_name (str): The name of the table to insert data into.
        - column_name (str): The name of the column to insert data into.
        - data (Any): The data to insert.
    
    Returns:
        - None
    '''
    conn, cursor = open_database(db_path)
    cursor.execute(f"INSERT INTO {table_name} ({column_name}) VALUES (?)", (data))
    close_database(conn)

def retrieve_table_data(db_path: str, table_name: str) -> pd.DataFrame:
    '''
    Retrieves the data from the specified table in the database.
    
    Parameters:
        - db_path (str): The path to the database file.
        - table_name (str): The name of the table to retrieve data from.
    
    Returns:
        - pd.DataFrame: The retrieved data as a pandas DataFrame.
    '''
    conn, cursor = open_database(db_path)
    cursor.execute(f"SELECT * FROM {table_name}")
    df = pd.DataFrame(cursor.fetchall(), columns=[column[0] for column in cursor.description])
    close_database(conn)
    return df

def create_dataframe(table_name: str) -> pd.DataFrame:
    """
    Create a dataframe from the specified table and return it.

    Parameters:
        - table_name (str): The name of the table from which to create the dataframe.

    Returns:
        - pd.DataFrame: The dataframe created from the specified table.
    """
    conn, cursor = open_database(config.database_path)
    cursor.execute(f"SELECT * FROM {table_name}")
    df = pd.DataFrame(cursor.fetchall(), columns=[column[0] for column in cursor.description])
    close_database(conn)
    return df

if __name__ == '__main__':
    print("Creating dataframe...")