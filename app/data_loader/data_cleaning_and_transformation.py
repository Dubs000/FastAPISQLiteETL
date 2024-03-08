import pandas as pd
from typing import Union
import re


def is_valid_email(email):
    if email:  # Check if email is not None or empty
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))
    return False


def is_valid_rating(rating):
    return rating >= 0


class MissingColumns(Exception):
    pass


class InvalidColumnDtype(Exception):
    pass


def read_csv(filename: str) -> pd.DataFrame:
    return pd.read_csv(filename)


def convert_col_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a new pd.DataFrame object with column names more appropriate for database use
    :param df - Input DataFrame with inappropriate column names
    :return: new_df - DataFrame with transformed column names
    """
    new_df = df.copy()  # Work on a copy of the DataFrame
    new_col_names = [col.strip().lower().replace(" ", "_") for col in new_df.columns]
    new_df.columns = new_col_names
    return new_df


def validate_and_convert_dtypes(df: pd.DataFrame, expected_datatypes: dict) -> Union[pd.DataFrame, InvalidColumnDtype]:
    """
    Returns bool based on whether the columns have the correct data types
    :param df: input dataframe
    :param expected_datatypes - mapping of columns to their expected datatype
    :return: True | InvalidColumnDtypes
    """
    new_df = df.copy()
    missing_columns = []
    for column, expected_dtype in expected_datatypes.items():
        if column in new_df.columns:
            actual_dtype = new_df[column].dtype
            if actual_dtype != expected_dtype:
                print(f"Converting {column} from {actual_dtype} to {expected_dtype}")
                # Exception potentially raised here
                new_df[column] = convert_column_dtype(new_df[column], expected_dtype)
        else:
            missing_columns.append(column)
            print(f"Warning: Expected column '{column}' not found in DataFrame")

    if missing_columns:
        raise MissingColumns(
            f"Missing columns in input data, please investigate, missing columns = {missing_columns}")
    return new_df


def convert_column_dtype(column, target_dtype):
    try:
        if target_dtype == 'datetime64[ns]':
            return pd.to_datetime(column, errors='coerce')
        elif target_dtype == 'object':
            # Strip whitespace from text based fields
            return column.str.strip().str.replace('\s+', ' ', regex=True).astype(str)
        else:
            return column.astype(target_dtype)
    except Exception as e:
        print(f"Error converting column: {e}")
        raise InvalidColumnDtype(f"Error converting column {column}: {e}")  # Return original column in case of error


def validate_input_datastructure_and_types(df: pd.DataFrame):
    expected_datatypes = {
        'reviewer_name': 'object', 'review_title': 'object', 'review_rating': 'int64', 'review_content': 'object',
        'email_address': 'object', 'country': 'object', 'review_date': 'datetime64[ns]'
    }
    corrected_table_name_df = convert_col_names(df)
    return validate_and_convert_dtypes(corrected_table_name_df, expected_datatypes)


def clean_and_transform_data(df: pd.DataFrame) -> pd.DataFrame:

    # Standardise and capitalise reviewer_name field
    df['reviewer_name'] = df['reviewer_name'].str.strip().str.title()

    # Add columns email_valid and rating_valid that are boolean
    df['email_valid'] = df['email_address'].apply(is_valid_email)
    df['rating_valid'] = df['review_rating'].apply(is_valid_rating)

    # Get rows with invalid emails/ratings
    df_invalid_emails = df[~df['email_valid']]
    df_invalid_ratings = df[~df['rating_valid']]
    print(f"Dataframe contains invalid emails: {df_invalid_emails}")
    print(f"Dataframe contains invalid ratings: {df_invalid_ratings}")

    # Remove invalid ratings and emails by filtering where email_valid AND rating_valid are both True
    df = df[df['email_valid'] & df['rating_valid']]
    df.drop(columns=['email_valid', 'rating_valid'], inplace=True)  # Remove these boolean columns

    # Need further context on the data and use cases to determine whether to drop rows with NaN values for other fields
    return df


def prepare_data_for_loading(csv_file_name: str) -> pd.DataFrame:
    df = read_csv(csv_file_name)
    valid_df = validate_input_datastructure_and_types(df)
    return clean_and_transform_data(valid_df)


if __name__ == "__main__":
    csv_file_name = "../../data/reviews.csv"
    df = prepare_data_for_loading(csv_file_name)
