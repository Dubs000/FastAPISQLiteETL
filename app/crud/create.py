from app.database.database import create_connection


def insert_review(review_data):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reviews (reviewer_name, review_title, review_rating, review_content, email_address, country, review_date) 
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, review_data)
    conn.commit()
    conn.close()


def insert_reviews(reviews_data):
    pass
