# data/data_augmentation/data_query.py
"""
This file contains functions for querying and manipulating data in a SQLite database.

Functions include:

    - column_exists(db_path: str, table_name: str, column_name: str) - Check if a column exists in a table within a SQLite database.
    - is_column_empty_or_null(db_path: str, table_name: str, column_name: str) - Checks if any row in a specific column of a table in the database is empty or null.
    - find_all_duplicates(db_path: str, table_name: str, column_name: str) - Find all duplicates in a specific column of a table in the database.
    - add_database_column(db_path: str, table_name: str, column_name: str) - Add a new column to the specified table in the database.
    - drop_database_column(db_path: str, table_name: str, column_name: str) - Drops the specified column from the given database table.
    - delete_row_by_id(db_path: str, table_name: str, row_id: int) - Deletes the row with the specified ID from the specified table in the database.
    - rename_database_column(db_path: str, table_name: str, old_column_name: str, new_column_name: str) - Renames the specified column in the specified table in the database.
    - update_database_column(db_path: str, table_name: str, column_name: str, value: str) - Updates the value of the specified column in the specified table in the database.
    - update_database_cell(db_path: str, table_name: str, row_id: int, column_name: str, value: str | int) - Updates the value of the specified cell in the specified table in the database.
    - retrieve_id_from_database(db_path: str, table_name: str, column_name: str, value: str) - Retrieves a specified ID from the specified table in the database depending on the provided column and value.
    - insert_into_database(db_path: str, table_name: str, column_name: str, data: Any) - Insert data into the specified table in the database.
    - retrieve_table_data(db_path: str, table_name: str) - Retrieves the data from the specified table in the database.
    - create_dataframe(table_name: str) - Create a dataframe from the specified table and return it.
"""

from typing import Any

import pandas as pd

from file_setup import config
from file_setup.init_processing import open_database, close_database


def column_exists(db_path: str, table_name: str, column_name: str) -> bool:
    """
    Check if a column exists in a table within a SQLite database.

    Parameters:
        - db_path (str): The path to the database file.
        - table_name (str): The name of the table.
        - column_name (str): The name of the column to check.

    Returns:
        - bool: True if the column exists, False otherwise.
    """
    conn, cursor = open_database(db_path)

    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()

    for col in columns:
        if col[1] == column_name:
            close_database(conn)
            return True

    close_database(conn)
    return False


def is_column_empty_or_null(db_path: str, table_name: str, column_name: str) -> bool:
    """
    Checks if any row in a specific column of a table in the database is empty or null.

    Parameters:
        - db_path (str): The path to the database file.
        - table_name (str): The name of the table.
        - column_name (str): The name of the column to check.

    Returns:
        - bool: True if any row in the column is empty or null, False otherwise.
    """
    conn, cursor = open_database(db_path)
    cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} IS NULL OR {column_name} = ''")
    count = cursor.fetchone()[0]
    close_database(conn)
    return count > 0


def find_all_duplicates(db_path: str, table_name: str, column_names: list[str]) -> dict[tuple, list[int]]:
    """
    Find all duplicates in a specific column of a table in the database.

    Parameters:
        - db_path (str): The path to the database file.
        - table_name (str): The name of the table.
        - column_name (list[str]): The names of the column to check for duplicates.

    Returns:
        - dict[str, list[int]]: A dictionary with tuples of duplicated values as keys and lists of their corresponding row IDs as values.
    """
    conn, cursor = open_database(db_path)

    columns_str: str = ', '.join(column_names)

    cursor.execute(
        f"SELECT {columns_str}, COUNT(*), GROUP_CONCAT(id) FROM {table_name} GROUP BY {columns_str} HAVING COUNT(*) > 1")
    rows = cursor.fetchall()
    duplicates = {tuple(row[:-2]): [int(row_id) for row_id in row[-1].split(',')] for row in rows}

    close_database(conn)
    return duplicates


def add_database_column(db_path: str, table_name: str, column_name: str) -> None:
    """
    Add a new column to the specified table in the database.

    Parameters:
        - db_path (str): The path to the database file.
        - table_name (str): The name of the table to add the column to.
        - column_name (str): The name of the new column.

    Returns:
        - None
    """
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


def delete_row_by_id(db_path: str, table_name: str, row_id: int) -> None:
    """
    Delete a row from the specified table in the database based on the row ID.

    Parameters:
        - db_path (str): The path to the database file.
        - table_name (str): The name of the table.
        - row_id (int): The ID of the row to delete.

    Returns:
        - None
    """
    conn, cursor = open_database(db_path)
    cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (row_id,))
    conn.commit()
    close_database(conn)


def update_database_column(db_path: str, table_name: str, column_name: str, value: str | int) -> None:
    """
    Updates the value of the specified column in the specified table in the database.

    Parameters:
        - db_path (str): The path to the database file.
        - table_name (str): The name of the table to update.
        - column_name (str): The name of the column to update.
        - value (str): The new value for the column.

    Returns:
        - None
    """
    conn, cursor = open_database(db_path)
    cursor.execute(f"UPDATE {table_name} SET {column_name} = '{value}'")
    close_database(conn)


def update_database_cell(db_path: str, table_name: str, row_id: int, column_name: str, value: str | int) -> None:
    """
    Updates the value of the specified cell in the specified table in the database.

    Parameters:
        - db_path (str): The path to the database file.
        - table_name (str): The name of the table to update.
        - row_id (int): The ID of the row to update.
        - column_name (str): The name of the column to update.
        - value (str): The new value for the cell.

    Returns:
        - None
    """
    conn, cursor = open_database(db_path)
    cursor.execute(f"UPDATE {table_name} SET {column_name} = ? WHERE id = ?", (value, row_id))
    close_database(conn)


def retrieve_id_from_database(db_path: str, table_name: str, column_name: str, value: str) -> int | None:
    """
    Retrieves a specified ID from the specified table in the database depending on the provided column and value.

    Parameters:
        - db_path (str): The path to the database file.
        - table_name (str): The name of the table to retrieve the ID from.
        - column_name (str): The name of the column to filter by.
        - value (str): The value to filter by.

    Returns:
        - int: The retrieved ID.
    """
    conn, cursor = open_database(db_path)
    cursor.execute(f"SELECT id FROM {table_name} WHERE {column_name} = ?", (value,))
    row_id = cursor.fetchone()
    close_database(conn)
    return row_id[0] if row_id else None


def rename_database_column(db_path: str, table_name: str, old_column_name: str, new_column_name: str) -> None:
    """
    Renames the specified column in the specified table in the database.

    Parameters:
        - db_path (str): The path to the database file.
        - table_name (str): The name of the table to rename the column in.
        - old_column_name (str): The name of the column to be renamed.
        - new_column_name (str): The new name for the column.

    Returns:
        - None
    """
    conn, cursor = open_database(db_path)
    cursor.execute(f"ALTER TABLE {table_name} RENAME COLUMN {old_column_name} TO {new_column_name}")
    close_database(conn)


def insert_into_database(db_path: str, table_name: str, column_names: list[str], data: Any) -> None:
    """
    Insert data into the specified table in the database.

    Parameters:
        - db_path (str): The path to the database file.
        - table_name (str): The name of the table to insert data into.
        - column_name (str): The name of the column to insert data into.
        - data (Any): The data to insert.

    Returns:
        - None
    """
    conn, cursor = open_database(db_path)

    # noinspection PyTypeChecker
    placeholders = ', '.join(['?'] * len(column_names))
    columns = ', '.join(column_names)
    cursor.executemany(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", data)
    close_database(conn)


def retrieve_table_data(db_path: str, table_name: str) -> pd.DataFrame:
    """
    Retrieves the data from the specified table in the database.

    Parameters:
        - db_path (str): The path to the database file.
        - table_name (str): The name of the table to retrieve data from.

    Returns:
        - pd.DataFrame: The retrieved data as a pandas DataFrame.
    """
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
    conn, cursor = open_database(config.essay_db_path)
    cursor.execute(f"SELECT * FROM {table_name}")
    df = pd.DataFrame(cursor.fetchall(), columns=[column[0] for column in cursor.description])
    close_database(conn)
    return df


if __name__ == '__main__':
    print("Creating dataframe...")
