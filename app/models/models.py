from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

"""
This module defines all models for user inputs via the API
"""


class Condition(BaseModel):
    column: str
    equals: Optional[str] = None
    contains: Optional[str] = None
    range: Optional[List[str]] = None

    # Add custom validators as needed
    @field_validator('column')
    def validate_column_name(cls, v):
        # validate that column name is allowed
        return v
