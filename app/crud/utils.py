from app.database.database_logger import database_logger
from typing import List
from app.models.models import Condition, QueryInput, Review

"""
Parameterised queries are used here via the `?` syntax where the query is built and values supplied at
the time of execution of the query
Used to prevent SQL injections

Future functionality would include an `OR` operator as it is currently only able to do AND conditions
"""


def build_where_clause(conditions=List[Condition]):
    """
    Build where clause based on a set of conditions, this API only allows for operators
    `range`, `contains` and `equals` however is easily extensible to include other operators
    :param conditions:
    :return: `WHERE` clause
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
        # Add more condition types as needed to the `Condition` model

    where_clause = " AND ".join(where_clauses) if where_clauses else ""
    database_logger.info(f"Generated where clause = `{where_clause}`, Params = `{params}`")
    return where_clause, params


def build_select_query_(query_input=QueryInput, where_clause="", params=None):
    base_query = f"SELECT {', '.join(query_input.columns) if query_input.columns else '*'} FROM {query_input.table}"

    if where_clause:
        base_query += " WHERE " + where_clause
    if query_input.limit:
        base_query += " LIMIT ?"
        params.append(query_input.limit)
    database_logger.info(f"Generated select clause = `{base_query}`, Params = `{params}`")
    return base_query, params if params else []


def build_select_query(query_input: QueryInput):
    where_clause_generated, params_generated = build_where_clause(query_input.conditions)
    base_query, params = build_select_query_(
        query_input,
        where_clause_generated,
        params_generated,
        )
    return base_query, params


def build_update_query(table, update_fields, conditions):
    set_clause = ", ".join([f"{key} = ?" for key in update_fields.keys()])
    where_clause, where_params = build_where_clause(conditions)

    query = f"UPDATE {table} SET {set_clause}"
    if where_clause:
        query += " WHERE " + where_clause

    params = list(update_fields.values()) + where_params
    return query, params


if __name__ == "__main__":
    conditions_ = [
        Condition(column="review_date", range=["2021-01-01", "2021-01-31"]),
        Condition(column="reviewer_name", contains="John")
    ]
    where_clause_, params_ = build_where_clause(conditions_)
    query_input = QueryInput(table="reviews", columns=["review_date", "reviewer_name"], conditions=conditions_, limit=5)
    q, p = build_select_query(query_input)