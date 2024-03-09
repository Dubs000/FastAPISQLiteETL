from app.database.database import create_connection
from app.database.database_logger import database_logger
from app.crud.utils import build_where_clause, build_select_query
from app.models.models import QueryInput


def get_all_reviews():
    conn = create_connection()
    cursor = conn.cursor()
    select_query, params = build_select_query(QueryInput(table="reviews"))
    cursor.execute(select_query, params)
    reviews = cursor.fetchall()
    conn.close()
    return reviews


def run_select_query(query_input: QueryInput):
    conn = create_connection()
    cursor = conn.cursor()
    select_query, params = build_select_query(query_input)
    cursor.execute(select_query, params)
    reviews = cursor.fetchall()
    conn.close()
    return reviews


def search_reviews_containing():
    # Search review based on a text field
    pass


def get_reviews_by_date():
    pass


if __name__ == "__main__":
    get_all_reviews()
