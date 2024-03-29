# data\data_maintenance\maintain.py
"""
This module contains functions for data maintenance.

Functions include:
    - generate_health_report(db_path: str, table_name: str, duplicates: list, empty_or_null_columns: list, actions_taken: dict)
        Generates a health report of the database after maintenance operations.
    - resolve_duplicates(database: str, table_name: str, duplicates: dict[str | tuple, list[int]])
        Resolve duplicates in a table in the database. Doesn't resolve the first row of each duplicate group.
    - main()
        Runs the data maintenance process. Note: May require user input.
"""

import data.data_augmentation.data_query as dq
from file_setup.config import essay_db_path, essay_health_path, log_path, test_db_path
from file_setup.init_processing import open_database, close_database


def generate_health_report(db_path: str, table_name: str, duplicates: list, empty_or_null_columns: list,
                           actions_taken: dict):
    """
    Generates a health report of the database after maintenance operations.

    Parameters:
        - db_path (str): The path to the database file.
        - table_name (str): The name of the table.
        - duplicates (list): A list of columns with duplicates.
        - empty_or_null_columns (list): A list of columns with empty or null values.
        - actions_taken (dict): A dictionary of actions taken during maintenance.

    Returns:
        None: Outputs the health report to the console or a file.
    """
    if table_name == 'essays':
        log_file: str = essay_health_path
    else:
        log_file: str = log_path

    report: str = f"Database Health Report for '{table_name}' in '{db_path}':\n\n"

    report += "1. Duplicates:\n"
    if duplicates:
        report += f"   - Duplicate columns: {', '.join([' & '.join(map(str, dup)) for dup in duplicates])}\n"
    else:
        report += "   - No duplicates found.\n"

    report += "\n2. Empty or Null Columns:\n"
    if empty_or_null_columns:
        report += f"   - Columns with empty or null values: {', '.join(empty_or_null_columns)}\n"
    else:
        report += "   - No empty or null columns found.\n"

    report += "\n3. Actions Taken:\n"
    for action, details in actions_taken.items():
        report += f"   - {action}: {details}\n"

    report += "\nEnd of Report\n"

    print(report)

    with open(log_file, 'a') as f:
        f.write(report)


def resolve_duplicates(database: str, table_name: str, duplicates: dict[str | tuple, list[int]]) -> list[str]:
    """
    Resolve duplicates in a table in the database. Doesn't resolve the first row of each duplicate group.
    
    Parameters: - database (str): The path to the database file. - table_name (str): The name of the table. -
    duplicates (dict[str | tuple, list[int]]): A dictionary with duplicated values as keys and lists of their corresponding row IDs as values.
    
    Returns:
        - log (str): A log of the actions taken.
    """
    log: list[str] = []

    for (column_1, column_2), row_ids in duplicates.items():
        row_ids_to_delete: list[int] = sorted(row_ids)[1:]

        for row_id in row_ids_to_delete:
            dq.delete_row_by_id(database, table_name, row_id)
            message: str = f"Resolved duplicate for '{column_1}' ({column_2}) with row ID {row_id}"
            log.append(message)

    return log


def main():
    # Configure the table_name here
    table_name = 'essays'

    empty_or_null_columns = []
    actions: dict[str, str | list[str]] = {}
    if table_name == 'essays':
        database = essay_db_path
    else:
        database = test_db_path

    conn, cursor = open_database(database)
    duplicates = dq.find_all_duplicates(database, table_name, ['title', 'year'])
    if duplicates:
        log = resolve_duplicates(database, table_name, duplicates)
        actions['Resolve duplicates'] = log
    else:
        actions['Resolve duplicates'] = 'No duplicates found.'

    database_columns: list[str] = cursor.execute(f"PRAGMA table_info({table_name})").fetchall()

    for column in database_columns:
        column_name = column[1]
        if dq.column_exists(database, table_name, column_name) and dq.is_column_empty_or_null(database, table_name,
                                                                                              column_name):
            user_input = input(
                f"Column '{column_name}' in table '{table_name}' in database '{database}' is empty or null. "
                "Are you sure you want to remove it? (y/n): "
            )
            if user_input.lower() == 'y':
                print(f"Removing empty or null column: {column_name}")
                empty_or_null_columns.append(column_name)
                dq.drop_database_column(database, table_name, column_name)
                actions[
                                'Remove empty or null column: ' + column_name] = f"ALTER TABLE {table_name} DROP COLUMN {column_name}"
            else:
                print(f"Skipping empty or null column: {column_name}")
                actions[
                        'Skip empty or null column: ' + column_name] = f"Skipping empty or null column: {column_name}"

    generate_health_report(database, table_name, duplicates, empty_or_null_columns, actions)
    close_database(conn)


if __name__ == '__main__':
    main()
