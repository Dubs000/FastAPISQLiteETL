import sqlite3
from app.database.database import create_connection
"""
Delete a Review: 
Remove a specific review from the database, typically identified by a unique ID.

Delete Reviews by User: 
Remove all reviews submitted by a specific user.

Bulk Delete: 
A more advanced operation that allows deletion of reviews based on certain filters, 
such as all reviews before a certain date or all reviews with a rating below a certain threshold.
"""


def delete_all_reviews():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM reviews where 1 = 1;")
    conn.commit()
    conn.close()
