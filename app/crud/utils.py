from app.database.database_logger import database_logger
from typing import List
from app.models.models import Condition, QueryInput, ColumnToUpdate

"""
This module provides utility functions to build SQL clauses for various database operations.
It leverages parameterized queries to prevent SQL injection and currently supports 'AND' conditions.
Future improvements may include the addition of 'OR' operators.
"""

def build_update_clause(table_name: str, conditions: List[Condition], columns_to_update: List[ColumnToUpdate]):
    """
    Constructs an SQL UPDATE statement with SET and WHERE clauses.

    Args:
        table_name (str): The name of the table to update.
        conditions (List[Condition]): A list of conditions to filter the rows to update.
        columns_to_update (List[ColumnToUpdate]): A list of columns and their new values to update.

    Returns:
        tuple: A tuple containing the SQL update statement and parameters.
    """
    where_clause, where_clause_params = build_where_clause(conditions)

    set_clauses = []
    set_clause_params = []
    for col_to_update in columns_to_update:
        set_clauses.append(f"{col_to_update.column_name} = ?")
        set_clause_params.append(col_to_update.column_value)
    set_clause_str = ", ".join(set_clauses)

    # Combine the SET and WHERE clause parameters in order
    update_params = set_clause_params + where_clause_params

    return f"UPDATE {table_name} SET {set_clause_str} WHERE {where_clause}", update_params

def build_where_clause(conditions=List[Condition]):
    """
    Builds a WHERE clause for SQL queries based on specified conditions.

    Args:
        conditions (List[Condition]): Conditions to include in the WHERE clause.

    Returns:
        tuple: A tuple containing the WHERE clause and associated parameters.
    """
    where_clauses = []
    params = []

    for condition in conditions:
        if condition.range:
            where_clauses.append(f"{condition.column} BETWEEN ? AND ?")
            params.extend(condition.range)
        elif condition.contains:
            where_clauses.append(f"{condition.column} LIKE ?")
            params.append(f"%{condition.contains}%")
        elif condition.equals:
            where_clauses.append(f"{condition.column} = ?")
            params.append(condition.equals)

    where_clause = " AND ".join(where_clauses) if where_clauses else ""
    database_logger.info(f"Generated WHERE clause: `{where_clause}`, Params: `{params}`")
    return where_clause, params

def build_select_query_(query_input=QueryInput, where_clause="", params=None):
    """
    Constructs a SELECT SQL query.

    Args:
        query_input (QueryInput): Object containing query parameters.
        where_clause (str): The WHERE clause for the query.
        params (List): Parameters for the WHERE clause.

    Returns:
        tuple: The SQL SELECT query and parameters.
    """
    base_query = f"SELECT {', '.join(query_input.columns) if query_input.columns else '*'} FROM {query_input.table}"

    if where_clause:
        base_query += " WHERE " + where_clause
    if query_input.limit:
        base_query += " LIMIT ?"
        params.append(query_input.limit)
    database_logger.info(f"Generated SELECT query: `{base_query}`, Params: `{params}`")
    return base_query, params if params else []

def build_select_query(query_input: QueryInput):
    """
    Builds a complete SELECT query using query input.

    Args:
        query_input (QueryInput): An object encapsulating the table, columns, conditions, and limit for the query.

    Returns:
        tuple: A complete SQL SELECT statement and its parameters.
    """
    where_clause_generated, params_generated = build_where_clause(query_input.conditions)
    base_query, params = build_select_query_(
        query_input,
        where_clause_generated,
        params_generated
    )
    return base_query, params

# Example use cases for demonstration
if __name__ == "__main__":
    # Define conditions for the WHERE clause
    conditions_ = [
        Condition(column="review_date", range=["2021-01-01", "2021-01-31"]),
        Condition(column="reviewer_name", contains="John")
    ]
    # Build the WHERE clause and prepare the query
    where_clause_, params_ = build_where_clause(conditions_)
    query_input = QueryInput(table="reviews", columns=["review_date", "reviewer_name"], conditions=conditions_, limit=5)
    # Generate the final SELECT query
    q, p = build_select_query(query_input)
