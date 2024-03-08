import sqlite3
import os


# Construct an absolute path to the database file
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Use this path when connecting to the database
db_path = os.path.join(base_dir, 'database/trustpilot_reviews.db')


def create_connection():
    return sqlite3.connect(db_path)


def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            reviewer_name TEXT,
            review_title TEXT,
            review_rating INTEGER,
            review_content TEXT,
            email_address TEXT,
            country TEXT,
            review_date TEXT
        );
    """)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()

