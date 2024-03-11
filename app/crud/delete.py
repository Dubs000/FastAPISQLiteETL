from sqlite3 import Error as SQLiteError

from app.database.database import create_connection
from app.database.database_logger import database_logger
from app.models.models import Condition
from app.crud.utils import build_where_clause

from typing import List


def delete_reviews(conditions: List[Condition]):
    with create_connection() as conn:
        try:
            cursor = conn.cursor()
            where_clause, params = build_where_clause(conditions)
            delete_statement = f"DELETE FROM reviews WHERE {where_clause}"
            database_logger.info(f"Executing delete statement: {delete_statement}")

            cursor.execute(delete_statement, params)
            rows_deleted = cursor.rowcount  # Number of rows deleted
            conn.commit()

            database_logger.info(f"Number of rows deleted: {rows_deleted}")
            return rows_deleted
        except SQLiteError as error:
            database_logger.error(f"Failed to delete data: {error}")
            return None


if __name__ == "__main__":
    condition = Condition(column="reviewer_name", equals='John Doe')
    conditions = [condition]
    delete_reviews(conditions)

