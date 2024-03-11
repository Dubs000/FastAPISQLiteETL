from typing import List, Optional, Union
from pydantic import BaseModel, Field, EmailStr, validator
from country_converter import convert
from datetime import date

"""
This module defines models representing various data structures used for user input validation in the API.
It includes models for a review, conditions for querying data, columns for updates, and overall query input.
"""


class Review(BaseModel):
    """
    A model representing a review, including details like reviewer's name, title, rating, etc.

    Attributes:
        reviewer_name (str): Name of the person who wrote the review.
        review_title (str): Title of the review.
        review_rating (int): Numerical rating given in the review.
        review_content (str): The content of the review.
        email_address (EmailStr): Email address of the reviewer.
        country (str): Country of the reviewer.
        country_code (str): ISO3 country code, automatically determined from the country.
        review_date (date): Date when the review was written.
    """
    reviewer_name: str
    review_title: str
    review_rating: int = Field(None, ge=1)
    review_content: str
    email_address: EmailStr
    country: str
    country_code: str = None  # To be populated by the validator
    review_date: date

    @validator('country')
    def convert_country_to_short_name(cls, v):
        """
        Validator to convert and validate the country name to its short name.

        Args:
            v (str): The country name to be converted and validated.

        Returns:
            str: The standardized short name of the country.

        Raises:
            ValueError: If the country name is not found in the conversion list.
        """
        standardized_country = convert(names=v, to='short_name')
        if standardized_country == 'not found':
            raise ValueError(f'Invalid country: {v}')
        return standardized_country

    @validator('country_code', pre=True, always=True)
    def set_country_code(cls, v, values):
        """
        Validator to set the ISO3 country code based on the country field.

        Args:
            v: The original value of country_code (not used in this case).
            values: The dictionary of field values.

        Returns:
            str: The ISO3 country code corresponding to the country.

        Raises:
            ValueError: If the country name does not have a corresponding ISO3 code.
        """
        country = values.get('country', None)
        if country:
            iso3_code = convert(names=country, to='ISO3')
            if iso3_code == 'not found':
                raise ValueError(f'Invalid country for code: {country}')
            return iso3_code
        return v

class Condition(BaseModel):
    """
    Represents a condition used in querying the database.

    Attributes:
        column (str): The column on which the condition is applied.
        equals (Optional[str]): The exact value the column should match.
        contains (Optional[str]): A substring the column should contain.
        range (Optional[List[str]]): A range (start and end) of values for the column.
    """
    column: str
    equals: Optional[str] = None
    contains: Optional[str] = None
    range: Optional[List[str]] = None

class ColumnToUpdate(BaseModel):
    """
    Represents a column to update in the database.

    Attributes:
        column_name (str): The name of the column to be updated.
        column_value (Union[str, int, EmailStr, date]): The new value for the column.
    """
    column_name: str
    column_value: Union[str, int, EmailStr, date]

class QueryInput(BaseModel):
    """
    Represents an input structure for database queries.

    Attributes:
        table (str): The name of the table to query.
        columns (Optional[List[str]]): A list of columns to retrieve.
        conditions (List[Condition]): Conditions to filter the query results.
        limit (Optional[int]): The maximum number of results to return.
    """
    table: str
    columns: Optional[List[str]] = None
    conditions: List[Condition] = []
    limit: Optional[int] = Field(None, ge=1)  # Must be greater than or equal to 1



if __name__ == "__main__":
    rev = Review(
        reviewer_name="Danny Walters",
        review_title="excellent",
        review_rating=1,
        review_content="some content",
        email_address="danny@gmail.com",
        country="USA",
        review_date=date(2023, 3, 3)
    )
    Condition(column="hello")
    breakpoint()
