
from app.data_loader.data_cleaning_and_transformation import prepare_data_for_loading
from app.database.database import base_dir


def test_data_loading(test_db):
    test_data_file = f"{base_dir.replace('app', '')}/tests/test_reviews.csv"
    df = prepare_data_for_loading(test_data_file)
    df.to_sql("reviews", test_db, if_exists='append', index=False)

    # Validate data
    cursor = test_db.cursor()
    cursor.execute("SELECT * FROM reviews;")
    data = cursor.fetchall()

    expected_row_count = 16
    assert len(data) == expected_row_count
