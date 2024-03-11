import pandas as pd
from typing import Union
import re
import country_converter as coco

from app.data_loader.data_loader_logger import data_loader_logger

cc = coco.CountryConverter()


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
    """
    Converts the data type of a pandas Series (column) to a specified target data type.

    Args:
        column (pd.Series): The column to be converted.
        target_dtype (str): The target data type as a string.

    Returns:
        pd.Series: The converted column.

    Raises:
        InvalidColumnDtype: If the conversion process encounters an error.
    """
    try:
        if target_dtype == 'dt.date':
            # Convert to datetime and then to date (without time)
            return pd.to_datetime(column, errors='coerce').dt.date
        elif target_dtype == 'object':
            # Clean string fields: strip whitespace and replace multiple spaces with a single space
            return column.str.strip().str.replace('\s+', ' ', regex=True).astype(str)
        else:
            # For other data types, use direct conversion
            return column.astype(target_dtype)
    except Exception as e:
        error_msg = f"Error converting column: {e}"
        data_loader_logger.error(error_msg)
        raise InvalidColumnDtype(error_msg)


def validate_input_datastructure_and_types(df: pd.DataFrame):
    """
    Validates and converts the data types of DataFrame columns to expected types.

    Args:
        df (pd.DataFrame): The DataFrame whose columns are to be validated and converted.

    Returns:
        pd.DataFrame: A DataFrame with columns converted to the expected data types.

    Note:
        This function expects a specific set of columns with defined target data types.
    """
    # Define the expected data types for each column
    expected_datatypes = {
        'reviewer_name': 'object',
        'review_title': 'object',
        'review_rating': 'int64',
        'review_content': 'object',
        'email_address': 'object',
        'country': 'object',
        'review_date': 'dt.date'
    }
    data_loader_logger.info(f"Mapping of expected datatype: {expected_datatypes}")

    # Convert column names to a consistent format
    corrected_table_name_df = convert_col_names(df)

    # Validate and convert data types of the DataFrame
    return validate_and_convert_dtypes(corrected_table_name_df, expected_datatypes)


def is_valid_email(email):
    if email:  # Check if email is not None or empty
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))
    return False


def is_valid_rating(rating):
    return rating >= 0


def convert_country_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts the country names in a DataFrame to standardized short names and ISO3 codes.

    The function uses the country_converter package to perform the conversion. If a country name
    cannot be matched, it is replaced with "Not Found".

    Args:
        df (pd.DataFrame): The DataFrame with a 'country' column containing country names.

    Returns:
        pd.DataFrame: A new DataFrame where the 'country' column contains standardized
                      short names and a new 'country_code' column contains ISO3 country codes.
    """
    new_df = df.copy()
    data_loader_logger.info("Converting 'country' column values to standardized short names.")
    country_names = cc.pandas_convert(series=new_df["country"], to='name_short', not_found="Not Found")

    data_loader_logger.info("Converting 'country' column values to standardized ISO3 country codes.")
    country_codes = cc.pandas_convert(series=new_df["country"], to='ISO3', not_found="Not Found")

    new_df["country"] = country_names
    new_df["country_code"] = country_codes
    return new_df


def validate_emails_and_ratings(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validates email addresses and review ratings in the DataFrame and removes invalid entries.

    This function adds two boolean columns, `email_valid` and `rating_valid`, to the DataFrame.
    It then filters out rows where emails are invalid or ratings are not meeting the criteria.

    Args:
        df (pd.DataFrame): The DataFrame containing the email addresses and review ratings.

    Returns:
        pd.DataFrame: A new DataFrame with invalid email addresses and ratings removed.

    Note:
        The function assumes the existence of `email_address` and `review_rating` columns in the DataFrame.
    """
    new_df = df.copy()
    # Validate email addresses using regex pattern
    data_loader_logger.info("Validating email addresses via regex pattern.")
    new_df['email_valid'] = new_df['email_address'].apply(is_valid_email)

    # Validate review ratings to ensure they meet certain criteria
    data_loader_logger.info("Validating review ratings.")
    new_df['rating_valid'] = new_df['review_rating'].apply(is_valid_rating)

    # Log and identify invalid emails and ratings
    df_invalid_emails = new_df[~new_df['email_valid']]
    df_invalid_ratings = new_df[~new_df['rating_valid']]
    if not df_invalid_emails.empty:
        data_loader_logger.warn(f"Dataframe contains invalid emails, which will be removed: \n{df_invalid_emails}")
    if not df_invalid_ratings.empty:
        data_loader_logger.warn(f"Dataframe contains invalid ratings, which will be removed: \n{df_invalid_ratings}")

    # Remove rows with invalid emails or ratings
    new_df = new_df[new_df['email_valid'] & new_df['rating_valid']]
    # Drop helper columns used for validation
    new_df.drop(columns=['email_valid', 'rating_valid'], inplace=True)
    return new_df



def clean_and_transform_data(df: pd.DataFrame) -> pd.DataFrame:

    country_transformed_df = convert_country_names(df)

    # Standardise and capitalise reviewer_name field
    data_loader_logger.info(f"Stripping whitespace and titling reviewer name")
    country_transformed_df['reviewer_name'] = country_transformed_df['reviewer_name'].str.strip().str.title()

    email_transformed_df = validate_emails_and_ratings(country_transformed_df)
    # Need further context on the data and use cases to determine whether to drop rows with NaN values for other fields
    return email_transformed_df


def prepare_data_for_loading(csv_file_name: str) -> pd.DataFrame:
    df = read_csv(csv_file_name)
    valid_df = validate_input_datastructure_and_types(df)
    return clean_and_transform_data(valid_df)


if __name__ == "__main__":
    csv_file_name = "../../data/reviews.csv"
    df = prepare_data_for_loading(csv_file_name)
