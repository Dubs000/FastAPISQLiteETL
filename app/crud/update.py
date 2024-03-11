from typing import List
from sqlite3 import Error as SQLiteError


from app.database.database import create_connection
from app.database.database_logger import database_logger
from app.crud.utils import build_update_clause
from app.models.models import Condition, ColumnToUpdate


"""
Edit a Review: 
Update details of an existing review, identified by a unique ID or a combination of reviewer name and review date.

Batch Update Reviews: 
A more advanced feature allowing the updating of multiple reviews at once based on certain criteria, 
like updating all reviews from a specific user.
"""


def update_review(conditions:List[Condition], columns_to_update: List[ColumnToUpdate]):
    set_clause, update_params = build_update_clause("reviews",
                                                                             conditions,
                                                                             columns_to_update)
    with create_connection() as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(set_clause, update_params)
            rows_updated = cursor.rowcount  # Number of rows deleted
            conn.commit()
            return rows_updated
        except SQLiteError as error:
            database_logger.error(f"An error occurred whilst trying to update `reviews` table: {error}")
            return None


if __name__ == "__main__":
    condition = Condition(column="country", equals='United States')
    column_to_update = ColumnToUpdate(column_name="reviewer_name", column_value="Splanny Walters")
    column_to_update_2 = ColumnToUpdate(column_name="country", column_value="United Kingdom")
    updated_rows = update_review([condition], [column_to_update, column_to_update_2])



