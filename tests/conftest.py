import pytest
import tempfile
import sqlite3
from fastapi.testclient import TestClient

from app.database.database import CREATE_TABLE_SQL
from app.routes.main import app


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def test_db(test_client):
    # Create a temporary file to use as a file-based SQLite database
    with tempfile.NamedTemporaryFile() as db_file:
        conn = sqlite3.connect(db_file.name)  # Connect to the temporary SQLite database

        # Setup the database (e.g., create tables)
        conn.execute(CREATE_TABLE_SQL)

        # Truncate the table using the test client, if necessary
        truncate_response = test_client.delete("/reviews/truncate")
        assert truncate_response.status_code == 201  # Check truncation success

        yield conn  # Yield the connection for use in tests

        # The connection will be automatically closed when the temp file is deleted
        # Temp file is automatically deleted after exiting this block