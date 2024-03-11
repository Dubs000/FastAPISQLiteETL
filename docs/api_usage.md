
# Reviews API Documentation

This document provides details on how to interact with the Reviews API, which allows for creating, reading, updating, and deleting reviews from a database.

## Select Reviews

### Endpoint: `/reviews/select` (POST)

Select reviews from the database based on specified query parameters.

#### Example Request:

```bash
curl -X POST http://127.0.0.1:8000/reviews/select \
     -H "Content-Type: application/json" \
     -d '{
            "table": "reviews",
            "columns": ["review_date", "reviewer_name"],
            "conditions": [
                {"column": "reviewer_name", "contains": "John"}
            ],
            "limit": "4"
          }'
```

#### Parameters:

- `table`: The table to query from.
- `columns`: List of columns to include in the result.
- `conditions`: Filters to apply when selecting.
- `limit`: Maximum number of results to return.

---

## Insert Reviews

### Endpoint: `/reviews/insert` (POST)

Insert new reviews into the database.

#### Example Request:

```bash
curl -X POST http://127.0.0.1:8000/reviews/insert \
     -H "Content-Type: application/json" \
     -d '[{"reviewer_name": "Danny Walters", ...}, {...}]'
```

#### Parameters:

- A list of `Review` objects to be inserted.

---

## Truncate Reviews Table

### Endpoint: `/reviews/truncate` (DELETE)

Delete all reviews from the database.

#### Example Request:

```bash
curl -X DELETE http://127.0.0.1:8000/reviews/truncate
```

---

## Delete Specific Reviews

### Endpoint: `/reviews/delete` (DELETE)

Delete reviews from the database based on specified conditions.

#### Example Request:

```bash
curl -X DELETE http://127.0.0.1:8000/reviews/delete \
     -H "Content-Type: application/json" \
     -d '[{"column": "reviewer_name", "contains": "Danny"}]'
```

#### Parameters:

- `conditions`: Conditions to identify which reviews to delete.

---

## Update Reviews

### Endpoint: `/reviews/update` (PATCH)

Update reviews in the database based on specified conditions and update data.

#### Example Request:

```bash
curl -X PATCH http://127.0.0.1:8000/reviews/update \
     -H "Content-Type: application/json" \
     -d '{
            "conditions": [{"column": "id", "equals": "1"}],
            "columns_to_update": [{"column_name": "review_title", "column_value": "Updated Title"}]
          }'
```

#### Parameters:

- `conditions`: Conditions to identify which reviews to update.
- `columns_to_update`: Data for updating the reviews.
