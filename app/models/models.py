from typing import List, Optional, Union
from pydantic import BaseModel, Field, EmailStr, field_validator, validator
from country_converter import convert
from datetime import date

"""
This module defines all models for user inputs via the API
"""


class Review(BaseModel):
    reviewer_name: str
    review_title: str
    review_rating: int = Field(None, ge=1)
    review_content: str
    email_address: EmailStr
    country: str
    country_code: str = None  # Will be set by the validator
    review_date: date

    @validator('country')
    def convert_country_to_short_name(cls, v):
        # Code to convert and validate the country name
        standardized_country = convert(names=v, to='short_name')
        if standardized_country == 'not found':
            raise ValueError(f'Invalid country: {v}')
        return standardized_country

    @validator('country_code', pre=True, always=True)
    def set_country_code(cls, v, values):
        # Code to set country code based on the country field
        country = values.get('country', None)
        if country:
            iso3_code = convert(names=country, to='ISO3')
            if iso3_code == 'not found':
                raise ValueError(f'Invalid country for code: {country}')
            return iso3_code
        return v


class Condition(BaseModel):
    column: str
    equals: Optional[str] = None
    contains: Optional[str] = None
    range: Optional[List[str]] = None


class ColumnToUpdate(BaseModel):
    column_name: str
    column_value: Union[str, int, EmailStr, date]


class QueryInput(BaseModel):
    table: str
    columns: Optional[List[str]] = None
    conditions: List[Condition] = []
    limit: Optional[int] = Field(None, ge=1)  # Limit needs to be >= 1


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
