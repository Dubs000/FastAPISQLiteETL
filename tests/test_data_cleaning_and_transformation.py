from app.data_loader.data_cleaning_and_transformation import *
import pytest
import pandas as pd
import datetime as dt

TEST_DF = pd.DataFrame(data={
    "Col 1": [1, 2, 3],
    "Col 2": ['Hello', 'World', "!"],
    "Column 3": ['1', '2', '4'],
    "column_4": [5, 6, 7]
})


@pytest.mark.parametrize("email, expected", [
    ("reviews_task@trustpilot.com", True), ("reviews_tasktrustpilot.com", False)
])
def test_email_validator_pass(email, expected):
    # Action
    actual_outcome = is_valid_email(email)
    # Assertion
    assert actual_outcome == expected


def test_test_validate_and_convert_dtype_invalid_dtype():
    """
    Test fails as there is a column specified in the `expected_dtypes` that is not
    present in the test dataframe
    """
    # Set up
    expected_dtypes = {"integer_column": "int64",
                       "datetime_column": 'datetime64[ns]',
                       }
    datetime_strings = ["2024-02-23", "2024-02-24", "2024-02-22", "2024-02-21"]
    test_df = pd.DataFrame(data={
        "integer_column": ['hello', '2', '3', '4'],
        "datetime_column": datetime_strings,
    })
    expected_error_msg = ('Error converting column 0    hello\n'
                          '1        2\n'
                          '2        3\n'
                          '3        4\n'
                          'Name: integer_column, dtype: object: invalid literal for int() with base 10: '
                          "'hello'")
    with pytest.raises(InvalidColumnDtype) as exc_info:
        validate_and_convert_dtypes(test_df, expected_dtypes)


def test_validate_and_convert_dtype_missing_column():
    """
    Test fails as there is a column specified in the `expected_dtypes` that is not
    present in the test dataframe
    """
    # Set up
    expected_dtypes = {"integer_column": "int64",
                       "integer_column_strings": "object",
                       "datetime_column": 'datetime64[ns]',
                       "object_column": 'object'}
    datetime_strings = ["2024-02-23", "2024-02-24", "2024-02-22", "2024-02-21"]
    test_df = pd.DataFrame(data={
        "integer_column": ['1', '2', '3', '4'],
        "integer_column_strings": ['1', '2', '3', '4'],
        "datetime_column": datetime_strings,
    })
    missing_columns = ["object_column"]
    expected_error_msg = f"Missing columns in input data, please investigate, missing columns = {missing_columns}"
    with pytest.raises(MissingColumns) as exc_info:
        validate_and_convert_dtypes(test_df, expected_dtypes)
    assert str(exc_info.value) == expected_error_msg


def test_validate_and_convert_dtype():
    """
    Test to convert `datetime_column` from strings to `datetime64[ns]` datatype
    `integer_column` converted from object to int64
    Other datatypes will remain the same
    """
    # Set up
    expected_dtypes = {"integer_column": "int64",
                       "integer_column_strings": "object",
                       "datetime_column": 'dt.date',
                       "object_column": 'object'}
    datetime_strings = ["2024-02-23", "2024-02-24", "2024-02-22", "2024-02-21"]
    test_df = pd.DataFrame(data={
        "integer_column": ['1', '2', '3', '4'],
        "integer_column_strings": ['1', '2', '3', '4'],
        "datetime_column": datetime_strings,
        "object_column": ["hello", "world", "string", "type"]})
    expected_df = pd.DataFrame(data={
        "integer_column": [1, 2, 3, 4],
        "integer_column_strings": ['1', '2', '3', '4'],
        "datetime_column": [dt.datetime.now() for _ in range(4)],
        "object_column": ["hello", "world", "string", "type"]
    })
    actual_df = validate_and_convert_dtypes(test_df, expected_dtypes)
    assert actual_df['integer_column'].dtype == expected_df['integer_column'].dtype
    assert actual_df['integer_column_strings'].dtype == expected_df['integer_column_strings'].dtype
    assert actual_df['datetime_column'].dtype == "object"
    assert actual_df['object_column'].dtype == expected_df['object_column'].dtype


def test_convert_col_names():
    # Desired outcome
    expected_df = pd.DataFrame(data={
        "col_1": [1, 2, 3],
        "col_2": ['Hello', 'World', "!"],
        "column_3": ['1', '2', '4'],
        "column_4": [5, 6, 7]
    })

    # Execution
    actual_df = convert_col_names(TEST_DF)

    # Assertion
    pd.testing.assert_frame_equal(actual_df, expected_df)


def test_clean_and_transform_data():
    pass
