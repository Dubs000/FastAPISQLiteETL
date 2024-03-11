"""
update.py

This script defines the functionality to update review records in the database.
It supports both editing individual reviews and batch updating multiple reviews
based on specific criteria. This includes updating details of an existing review,
identified by unique identifiers like ID or a combination of reviewer name and
review date, as well as more advanced batch update operations.
"""

from typing import List
from sqlite3 import Error as SQLiteError
from app.database.database import create_connection
from app.database.database_logger import database_logger
from app.crud.utils import build_update_clause
from app.models.models import Condition, ColumnToUpdate


def update_review(conditions: List[Condition], columns_to_update: List[ColumnToUpdate]):
    """
    Updates review records in the database based on specified conditions and update parameters.

    Args:
        conditions (List[Condition]): Conditions to select which reviews to update.
        columns_to_update (List[ColumnToUpdate]): Specifications of which columns to update and their new values.

    Returns:
        int: The number of rows that were updated.
    """
    # Build the SQL update clause with provided conditions and columns to update
    set_clause, update_params = build_update_clause("reviews", conditions, columns_to_update)

    with create_connection() as conn:
        try:
            cursor = conn.cursor()
            database_logger.info(f"Executing UPDATE on `reviews`: {set_clause} with params {update_params}")
            cursor.execute(set_clause, update_params)
            rows_updated = cursor.rowcount  # Capture the number of rows affected by the update
            conn.commit()
            database_logger.info(f"Rows updated in `reviews`: {rows_updated}")
            return rows_updated
        except SQLiteError as error:
            # Log the error and return None if an SQLite error occurs
            database_logger.error(f"An error occurred whilst trying to update `reviews` table: {error}")
            return None


# Example usage of the function
if __name__ == "__main__":
    # Conditions and columns to update for demonstration purposes
    condition = Condition(column="country", equals='United States')
    column_to_update = ColumnToUpdate(column_name="reviewer_name", column_value="Splanny Walters")
    column_to_update_2 = ColumnToUpdate(column_name="country", column_value="United Kingdom")
    updated_rows = update_review([condition], [column_to_update, column_to_update_2])
    print(f"Number of updated rows: {updated_rows}")
