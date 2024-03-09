import pandas as pd
from typing import Union
import re
import country_converter as coco

from app.data_loader.data_loader_logger import data_loader_logger

cc = coco.CountryConverter()


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
    data_loader_logger.info(msg=f"Reading csv file into dataframe {filename}")
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
    data_loader_logger.info(f"Convering column names into standard snakecase format from {df.columns} to {new_col_names}")
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
                data_loader_logger.info(f"Converting {column} from {actual_dtype} to {expected_dtype}")
                # Exception potentially raised here
                new_df[column] = convert_column_dtype(new_df[column], expected_dtype)
        else:
            missing_columns.append(column)
            data_loader_logger.warn(f"Expected column '{column}' not found in DataFrame")

    if missing_columns:
        error_msg = f"Missing columns in input data, please investigate, missing columns = {missing_columns}"
        data_loader_logger.error(error_msg)
        raise MissingColumns(error_msg)
    return new_df


def convert_column_dtype(column, target_dtype):
    try:
        if target_dtype == 'dt.date':
            data_loader_logger.info(f"Converting ")
            return pd.to_datetime(column, errors='coerce').dt.date
        elif target_dtype == 'object':
            # Strip whitespace from text based fields
            return column.str.strip().str.replace('\s+', ' ', regex=True).astype(str)
        else:
            return column.astype(target_dtype)
    except Exception as e:
        error_msg = f"Error converting column: {e}"
        data_loader_logger.error(error_msg)
        raise InvalidColumnDtype(error_msg)  # Return original column in case of error


def validate_input_datastructure_and_types(df: pd.DataFrame):
    expected_datatypes = {
        'reviewer_name': 'object', 'review_title': 'object', 'review_rating': 'int64', 'review_content': 'object',
        'email_address': 'object', 'country': 'object', 'review_date': 'dt.date'
    }
    corrected_table_name_df = convert_col_names(df)
    data_loader_logger.info(f"Mapping of expected datatype: {expected_datatypes}")
    return validate_and_convert_dtypes(corrected_table_name_df, expected_datatypes)


def clean_and_transform_data(df: pd.DataFrame) -> pd.DataFrame:

    # Convert country names to short names if not found then view as "Not Found"
    data_loader_logger.info(f"Converting values in 'country' column to standardised country names")
    country_names = cc.pandas_convert(series=df["country"], to='name_short', not_found="Not Found")
    # Convert country names to ISO3 code if not found then view as "Not Found"
    data_loader_logger.info(f"Converting values in 'country' column to standardised ISO3 country names")
    country_codes = cc.pandas_convert(series=df["country"], to='ISO3', not_found="Not Found")
    df["country"] = country_names
    df["country_code"] = country_codes

    # Standardise and capitalise reviewer_name field
    data_loader_logger.info(f"Stripping whitespace and titling reviewer name")
    df['reviewer_name'] = df['reviewer_name'].str.strip().str.title()

    # Add columns email_valid and rating_valid that are boolean
    data_loader_logger.info(f"Validating email addresses via regex [^@]+@[^@]+\.[^@]+")
    df['email_valid'] = df['email_address'].apply(is_valid_email)
    data_loader_logger.info("Ensuring review ratings are > 0")
    df['rating_valid'] = df['review_rating'].apply(is_valid_rating)

    # Get rows with invalid emails/ratings
    df_invalid_emails = df[~df['email_valid']][["reviewer_name","email_address"]]
    df_invalid_ratings = df[~df['rating_valid']][["reviewer_name","review_rating"]]
    if not df_invalid_emails.empty:
        data_loader_logger.warn(f"Dataframe contains invalid emails: \n{df_invalid_emails}\n, these emails will be "
                                f"removed")
    if not df_invalid_ratings.empty:
        data_loader_logger.warn(f"Dataframe contains invalid ratings: \n{df_invalid_ratings}\n, these ratings will be "
                                f"removed")

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
