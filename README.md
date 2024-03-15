## Project Overview

This project is designed to ingest, process, and manage review data, offering a RESTful API for effective data handling. It facilitates operations like data ingestion from CSV files, data standardization, and CRUD operations via an intuitive API.

## **Key Features**

- **Data Ingestion**: Ingest review data from CSV files into a SQLite database.
- **Data Cleaning and Transformation**: Standardize country names and codes using the **`country-converter`** package.
- **CRUD Operations**: Facilitate Create, Read, Update, and Delete operations through a RESTful API.
- **Data Validation**: Validate user inputs using Pydantic models.

## **Technology Stack**

- **FastAPI**: For building the RESTful API.
- **SQLite**: As the database for storing review data.
- **Pandas**: For data manipulation and cleaning.
- **Pydantic**: For validating and modeling request/response data.
- **Country-Converter**: For converting and standardizing country names and codes

## Installation and Setup

```bash
# Clone the repository
git clone https://github.com/Dubs000/TrustpilotDataOpsTest.git
cd TrustpilotDataOpsTest

# Install dependencies using pipenv
pip install pipenv
pipenv install

# Activate the virtual environment
pipenv shell

```

## Usage

The project is equipped with convenient scripts to facilitate database operations and to start the server.

### Initialize the Database

```bash
pipenv run initialize_db

```

### Load Data

Load review data into the database:

```bash
pipenv run load_data data/reviews.csv

```

### Start the Server

Launch the FastAPI server:

```bash
pipenv run start_server

```

Or, to perform all steps in one go:

```bash
pipenv run start_app

```

Visit `http://localhost:8000` to access the API.

## Running Tests
To run the automated tests:

```bash
pipenv run pytest
```

## Contributing

Contributions to enhance and improve the project are welcome. Adhere to coding best practices and submit pull requests for review.

## Contact

For further inquiries or suggestions, feel free to reach out at dwdanielwalters@gmail.com