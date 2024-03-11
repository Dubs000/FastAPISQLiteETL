from app.database.database import create_connection
from app.database.database_logger import database_logger
from app.crud.utils import build_select_query
from app.models.models import QueryInput, Condition
from sqlite3 import Error as SQLiteError

def format_results_to_json(cursor):
    """
    Convert SQL query results from a cursor into a JSON-compatible dictionary format.

    Args:
        cursor (sqlite3.Cursor): A cursor object containing the results of a SQL query.

    Returns:
        dict: A dictionary where each key-value pair represents a column name and its value.
    """
    results = [dict((cursor.description[i][0], value)
               for i, value in enumerate(row)) for row in cursor.fetchall()]
    returned_set = results if results else {}
    database_logger.info(f"{len(returned_set)} results returned from query")
    return returned_set

def get_all_reviews():
    """
    Retrieve all reviews from the database.

    Returns:
        list: A list of dictionaries, each representing a review record.
    """
    select_query, params = build_select_query(QueryInput(table="reviews"))
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(select_query, params)
            results = format_results_to_json(cursor)
            return results
    except SQLiteError as error:
        database_logger.error(f"Failed to run sql query {select_query} with params {params}: {error}")
        return "Error"

def run_select_query(query_input: QueryInput):
    """
    Execute a SELECT SQL query based on the provided QueryInput object.

    Args:
        query_input (QueryInput): An object containing parameters for building a SELECT query.

    Returns:
        list: A list of dictionaries representing the query results.
    """
    select_query, params = build_select_query(query_input)
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(select_query, params)
            results = format_results_to_json(cursor)
            return results
    except SQLiteError as error:
        database_logger.error(f"Failed to run sql query: `{select_query}` with params `{params}`\nError: {error}")
        return "Error"

if __name__ == "__main__":
    # Example usage of run_select_query with specific conditions
    condition = Condition(column="country", equals='United States')
    condition_2 = Condition(column="review_date", equals='2024-02-23')
    results = run_select_query(QueryInput(table="reviews",
                                columns=["id", "review_date", "country", "reviewer_name"],
                                conditions=[condition, condition_2],
                                limit=2))
    print(results)


