from app.database.database import create_connection


def get_all_reviews():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reviews;")
    reviews = cursor.fetchall()
    conn.close()
    return reviews


def search_reviews_containing():
    # Search review based on a text field
    pass


def get_reviews_by_date():
    pass

