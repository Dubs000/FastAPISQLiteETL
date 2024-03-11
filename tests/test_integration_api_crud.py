# Sample data for testing
sample_reviews = [
    {
        "reviewer_name": "Danny Walters",
        "review_title": "Excellent Meal",
        "review_rating": 5,
        "review_content": "Good food",
        "email_address": "dwdanielwalters@gmail.com",
        "country": "United Kingdom",
        "review_date": "2024-03-03"
    },
    {
        "reviewer_name": "Jeff Bezos",
        "review_title": "Terrible company",
        "review_rating": 5,
        "review_content": "takes too long to order products",
        "email_address": "jeffbezos@amazon.com",
        "country": "United States",
        "review_date": "2024-03-03"
    },
    {
        "reviewer_name": "Alexa Johnson",
        "review_title": "Great Service",
        "review_rating": 4,
        "review_content": "The service was quick and friendly.",
        "email_address": "alexa.johnson@example.com",
        "country": "Canada",
        "review_date": "2024-04-15"
    },
    {
        "reviewer_name": "Samuel Lee",
        "review_title": "Lovely Ambiance",
        "review_rating": 4,
        "review_content": "Loved the atmosphere and decor at the restaurant.",
        "email_address": "samlee_2024@example.com",
        "country": "United Kingdom",
        "review_date": "2024-05-21"
    },
    {
        "reviewer_name": "Maria Garcia",
        "review_title": "Best Coffee in Town",
        "review_rating": 5,
        "review_content": "The coffee and pastries are absolutely delightful!",
        "email_address": "mgarcia@example.net",
        "country": "Australia",
        "review_date": "2024-06-10"
    },
]

# Sample condition for testing SELECT and DELETE operations
sample_condition = [
    {"column": "reviewer_name", "contains": "Danny"}
]

# Sample data for testing the UPDATE operation
sample_update_data = [
    {
        "column_name": "review_title",
        "column_value": "Updated Title"
    }
]





def test_read_all_reviews_initially_empty(test_db, test_client):
    url_select_rows = "/reviews/select"
    data = {
        "table": "reviews"
    }
    # Make a POST request to the API
    response = test_client.post(url_select_rows, json=data)
    assert response.status_code == 200
    assert response.json() == {}


def test_insert_reviews(test_db, test_client):
    """
    This test confirms that we are able to insert rows into the table and return back
    the number of records inserted

    Also confirms that we are able to query based on specific conditions
    """
    response = test_client.post("reviews/insert", json=sample_reviews)
    assert response.status_code == 201
    assert "inserted_ids" in response.json()
    response = response.json()
    inserted_ids = response["inserted_ids"]
    assert len(inserted_ids) == len(sample_reviews)  # Check if the number of inserted IDs matches the input data

    expected_info = {
        "review_title": "Great Service",
        "review_rating": 4,
        "review_content": "The service was quick and friendly.",
        "email_address": "alexa.johnson@example.com",
        "country": "Canada",
        "review_date": "2024-04-15"
    }
    d = {"table": "reviews",
         "columns": ['review_title', 'review_rating', 'review_content', 'email_address', 'country', 'review_date'],
         "conditions":
             [
                 {"column": "reviewer_name", "equals": "Alexa Johnson"}
             ]
         }
    response = test_client.post("reviews/select", json=d)
    inserted_row = response.json()[0]
    assert inserted_row == expected_info


def test_update_specific_reviews(test_db, test_client):
    """
    This test shows that we can update a specific row in the database,
    retrieve this row and the retrieved row is as expected

    """
    # Insert 1 record into table
    r = test_client.post("/reviews/insert", json=[sample_reviews[0]])
    assert len(r.json()['inserted_ids']) == 1


    response = test_client.patch("reviews/update", json={
        "conditions": sample_condition,
        "columns_to_update": sample_update_data
    })
    assert response.status_code == 201
    assert "num_updated_rows" in response.json()
    assert response.json()["num_updated_rows"] > 0

    expected_updated_row = {
        "review_title": "Updated Title",
    }
    d = {"table": "reviews",
         "columns": ['review_title'],
         "conditions":
             [
                 {"column": "reviewer_name", "contains": "Danny"}
             ]
         }
    response = test_client.post("/reviews/select", json=d)
    actual_updated_row = response.json()[0]
    assert actual_updated_row == expected_updated_row


def test_delete_specific_reviews(test_db, test_client):

    # Insert all rows into table
    inserted = test_client.post("/reviews/insert", json=sample_reviews)
    d = {"table": "reviews",
         "conditions":
             [
                 {"column": "reviewer_name", "contains": "Danny"}
             ]
         }
    # Confirm there is 1 record in the table with "Danny" in reviewer name
    response = test_client.post("reviews/select", json=d)
    assert len(response.json()) == 1

    # Delete rows that contain "Danny" in reviewer name
    response = test_client.request("DELETE", "/reviews/delete", json=sample_condition)
    assert response.status_code == 201
    assert "num_deleted_rows" in response.json()
    assert response.json()["num_deleted_rows"] == 1

    # Confirm no records in db where reviewer_name contains "Danny"

    response = test_client.post("reviews/select", json=d)
    assert len(response.json()) == 0

