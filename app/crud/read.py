from app.database.database import create_connection
from app.database.database_logger import database_logger
from app.crud.utils import build_where_clause, build_select_query
from app.models.models import QueryInput, Condition
from sqlite3 import Error as SQLiteError


def format_results_to_json(cursor):
    results = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
    returned_set = results if results else {}
    database_logger.info(f"{len(returned_set)} results returned from query")
    return returned_set


def get_all_reviews():
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            select_query, params = build_select_query(QueryInput(table="reviews"))
            cursor.execute(select_query, params)
            results = format_results_to_json(cursor)
            return results
    except SQLiteError as error:
        database_logger.error(f"Failed to run sql query {select_query} with params {params}: {error}")
        return "Error"


def run_select_query(query_input: QueryInput):
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            select_query, params = build_select_query(query_input)
            cursor.execute(select_query, params)
            results = format_results_to_json(cursor)
            return results
    except SQLiteError as error:
        database_logger.error(f"Failed to run sql query: `{select_query}` with params `{params}`\nError: {error}")
        return "Error"


if __name__ == "__main__":
    condition = Condition(column="country", equals='United States')
    condition_2 = Condition(column="review_date", equals='2024-02-23')
    results = run_select_query(QueryInput(table="reviews",
                                columns=["id", "review_date", "country", "reviewer_name"],
                                conditions=[condition, condition_2],
                                limit=2))
    breakpoint()

