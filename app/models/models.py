from typing import List, Optional
from pydantic import BaseModel

"""
This module defines all models for user inputs via the API
"""


class Condition(BaseModel):
    column: str
    equals: Optional[str] = None
    contains: Optional[str] = None
    range: Optional[List[str]] = None

class QueryInput(BaseModel):
    table: str
    columns: Optional[List[str]] = None
    conditions: List[Condition] = []

