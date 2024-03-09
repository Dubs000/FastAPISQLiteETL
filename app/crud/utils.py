"""
Parameterised queries are used here via the `?` syntax where the query is built and values supplied at
the time of execution of the query
Used to prevent SQL injections
"""


def build_where_clause(conditions):
    """
    Build where clause based on a set of conditions, this API only allows for operators
    `range`, `contains` and `equals` however is easily extensible to include other operators
    :param conditions:
    :return: `WHERE` clause
    """
    where_clauses = []
    params = []

    for condition in conditions:
        if "range" in condition:
            where_clauses.append(f"{condition['column']} BETWEEN ? AND ?")
            params.extend(condition["range"])
        elif "contains" in condition:
            where_clauses.append(f"{condition['column']} LIKE ?")
            params.append(f"%{condition['contains']}%")
        elif "equals" in condition:
            where_clauses.append(f"{condition['column']} = ?")
            params.append(condition["equals"])
        # Add more condition types as needed

    where_clause = " AND ".join(where_clauses) if where_clauses else ""
    return where_clause, params


def build_select_query(table, columns=None, where_clause="", params=None):
    base_query = f"SELECT {', '.join(columns) if columns else '*'} FROM {table}"

    if where_clause:
        base_query += " WHERE " + where_clause

    return base_query, params if params else []


def build_update_query(table, update_fields, conditions):
    set_clause = ", ".join([f"{key} = ?" for key in update_fields.keys()])
    where_clause, where_params = build_where_clause(conditions)

    query = f"UPDATE {table} SET {set_clause}"
    if where_clause:
        query += " WHERE " + where_clause

    params = list(update_fields.values()) + where_params
    return query, params
