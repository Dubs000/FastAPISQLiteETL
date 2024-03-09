from app.data_loader.data_cleaning_and_transformation import prepare_data_for_loading
from app.database.database import create_connection
from app.data_loader.data_loader_logger import data_loader_logger

import argparse


def load_data(table_name: str, csv_file_name: str):
    df = prepare_data_for_loading(csv_file_name)
    conn = create_connection()
    data_loader_logger.info(f"Expecting to load `{len(df)}` rows into `{table_name}`")
    res = df.to_sql(table_name, conn, if_exists='append', index=False)
    data_loader_logger.info(f"{res} rows loaded successfully")
    data_loader_logger.info(f"Closing connection")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load data into the SQLite database.")
    parser.add_argument('--file', required=True, help="Path to the CSV file")
    args = parser.parse_args()
    table_name = "reviews"
    load_data(table_name=table_name, csv_file_name=args.file)

