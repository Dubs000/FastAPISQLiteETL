from app.database.database import create_connection
from app.database.database_logger import database_logger
from sqlite3 import Error as SQLiteError
from app.models.models import Review
from typing import List


def insert_reviews(reviews: List[Review]):
    """
    Insert a list of reviews into the database.

    Args:
        reviews (List[Review]): A list of Review objects to be inserted.

    Returns:
        List[int]: A list of IDs for the newly inserted review rows.
    """
    inserted_ids = []
    with create_connection() as conn:
        try:
            cursor = conn.cursor()
            for review in reviews:
                # Prepare and execute the INSERT query for each review
                insert_query = """INSERT INTO reviews (reviewer_name, review_title, review_rating, review_content,
                                email_address, country, country_code, review_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
                params = [review.reviewer_name, review.review_title, review.review_rating,
                          review.review_content, review.email_address, review.country,
                          review.country_code, review.review_date]

                cursor.execute(insert_query, params)
                last_row_id = cursor.lastrowid  # ID of the last inserted row
                inserted_ids.append(last_row_id)  # Collect all inserted row IDs
                database_logger.info(f"Inserted row into `reviews` table where `id`={last_row_id}")

            conn.commit()
        except SQLiteError as error:
            database_logger.error(f"Failed to insert data into sqlite table: {error}")
            return None

    return inserted_ids


if __name__ == "__main__":
    # Example usage of insert_reviews
    reviews = [
        Review(
            reviewer_name="Danny Walters",
            review_title="Excellent Meal",
            review_rating=5,
            review_content="Good food",
            email_address="dwdanielwalters@gmail.com",
            country="United States",
            review_date="2024-03-03")
    ]
    res = insert_reviews(reviews)
