from app.database.database import create_table
from app.data_loader.load_data import load_data
import uvicorn


def initialize_and_load_data(csv_file_path=None):
    # Initialize the database
    create_table()

    # Optionally, load data
    if csv_file_path:
        load_data("reviews", csv_file_path)


if __name__ == "__main__":
    # Initialize and load data
    # You can hardcode the path or modify the script to accept command line arguments
    initialize_and_load_data("data/reviews.csv")

    # Start the FastAPI server
    uvicorn.run("app.routes.main:app", host="127.0.0.1", port=8000, reload=True)