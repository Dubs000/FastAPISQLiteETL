from app.database.database import create_connection
from app.database.database_logger import database_logger
from app.crud.utils import build_where_clause, build_select_query
from app.models.models import QueryInput, Condition


def format_results_to_dict(cursor):
    results = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
    returned_set = results if results else {}
    database_logger.info(f"{len(returned_set)} results returned from query")
    return returned_set


def get_all_reviews():
    conn = create_connection()
    cursor = conn.cursor()
    select_query, params = build_select_query(QueryInput(table="reviews"))
    cursor.execute(select_query, params)
    results = format_results_to_dict(cursor)
    conn.close()
    return results


def run_select_query(query_input: QueryInput):
    conn = create_connection()
    cursor = conn.cursor()
    select_query, params = build_select_query(query_input)
    cursor.execute(select_query, params)
    results = format_results_to_dict(cursor)
    conn.close()
    return results


if __name__ == "__main__":
    condition = Condition(column="country", equals='United States')
    condition_2 = Condition(column="review_date", equals='2024-02-23')
    results = run_select_query(QueryInput(table="reviews",
                                columns=["review_date", "country", "reviewer_name"],
                                conditions=[condition, condition_2],
                                limit=2))

