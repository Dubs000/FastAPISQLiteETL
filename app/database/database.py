import sqlite3
import os

from app.database.database_logger import database_logger


# Construct an absolute path to the database file
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Use this path when connecting to the database
db_path = os.path.join(base_dir, 'database/trustpilot_reviews.db')


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            reviewer_name TEXT,
            review_title TEXT,
            review_rating INTEGER,
            review_content TEXT,
            email_address TEXT,
            country TEXT,
            country_code TEXT,
            review_date DATE
        );"""

DROP_TABLE_SQL = "DROP TABLE reviews"


def create_connection():
    database_logger.info(f"Creating connection to database, {db_path}")
    return sqlite3.connect(db_path)


def drop_table():
    conn = create_connection()
    cursor = conn.cursor()
    database_logger.info(f"Dropping table via SQL \n---{DROP_TABLE_SQL};\n---")
    cursor.execute("""
        {DROP_TABLE_SQL};
    """)
    conn.commit()
    conn.close()


def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    database_logger.info(f"Creating table via SQL \n---{CREATE_TABLE_SQL}\n---")
    cursor.execute(CREATE_TABLE_SQL)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table()

