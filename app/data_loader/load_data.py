from app.data_loader.data_cleaning_and_transformation import prepare_data_for_loading
from app.database.database import create_connection
import argparse


def load_data(csv_file_name: str):
    df = prepare_data_for_loading(csv_file_name)
    conn = create_connection()
    df.to_sql("reviews", conn, if_exists='append', index=False)
    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load data into the SQLite database.")
    parser.add_argument('--file', required=True, help="Path to the CSV file")
    args = parser.parse_args()
    load_data(args.file)

