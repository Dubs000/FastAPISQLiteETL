from app.crud.utils import build_where_clause, build_select_query_, build_update_query
import pytest
from app.models.models import Condition, QueryInput


@pytest.mark.parametrize(
    "conditions, expected_where_clause, expected_params",
    [
        # Test case 1
        (
            [Condition(column="review_date", range=["2021-01-01", "2021-01-31"])],
            "review_date BETWEEN ? AND ?",
            ["2021-01-01", "2021-01-31"]
        ),
        # Test case 2
        (
            [
                Condition(column="review_date", range=["2021-01-01", "2021-01-31"]),
                Condition(column="reviewer_name", contains="John")
            ],
            "review_date BETWEEN ? AND ? AND reviewer_name LIKE ?",
            ["2021-01-01", "2021-01-31", "%John%"]
        )
    ]
)
def test_build_where_clause(conditions, expected_where_clause, expected_params):
    actual_where_clause, actual_params = build_where_clause(conditions)

    assert expected_where_clause == actual_where_clause
    assert expected_params == actual_params


@pytest.mark.parametrize(
    "query_input, where_clause_generated, params, expected_base_query, expected_params",
    [
        # Test case 1 - select * with where clause
        (
                QueryInput(table="reviews", columns=None),
                "review_date BETWEEN ? AND ?",
                ["2021-01-01", "2021-01-31"],
                "SELECT * FROM reviews WHERE review_date BETWEEN ? AND ?",
                ["2021-01-01", "2021-01-31"],
        ),
        # Test case 2 - select column names with where clause
        (
                QueryInput(table="reviews", columns=["review_date", "country"]),
                "review_date BETWEEN ? AND ? AND reviewer_name LIKE ?",
                ["2021-01-01", "2021-01-31", "%John%"],
                "SELECT review_date, country FROM reviews WHERE review_date BETWEEN ? AND ? AND reviewer_name LIKE ?",
                ["2021-01-01", "2021-01-31", "%John%"]
        ),
        # Test case 3 - select * with no where clause
        (
                QueryInput(table="reviews", columns=[]),
                "",
                [],
                "SELECT * FROM reviews",
                []
        )
    ]
)
def test_build_entire_select_query(query_input,
                                   where_clause_generated,
                                   params,
                                   expected_base_query,
                                   expected_params):
    actual_base_query, actual_params = build_select_query_(
        query_input,
        where_clause_generated,
        params
    )
    assert actual_base_query == expected_base_query
    assert actual_params == expected_params
