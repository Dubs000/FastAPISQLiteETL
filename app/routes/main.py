from fastapi import FastAPI, HTTPException, status, Body
from starlette.concurrency import run_in_threadpool  # Allows synchronous code to run async by using threads
from fastapi.responses import JSONResponse
from typing import List

from app.crud.create import insert_reviews
from app.crud.read import run_select_query
from app.crud.update import update_review
from app.crud.delete import delete_reviews

from app.routes.routes_logger import api_logger
from app.models.models import QueryInput, Review, Condition, ColumnToUpdate


app = FastAPI()


@app.post("/reviews/select")
async def run_query(query_input: QueryInput = Body(...)):
    """
    Select reviews from the database based on specified query parameters.

    Example curl command:
    curl -X POST http://127.0.0.1:8000/reviews/select \
         -H "Content-Type: application/json" \
         -d '{"table": "reviews",
            "columns": ["review_date", "reviewer_name"],
            "conditions": [
                {"column": "reviewer_name", "contains": "John"}
            ],
            "limit": "4"}'

    Args:
        query_input (QueryInput): Query parameters for selecting reviews.

    Returns:
        JSONResponse: A response containing the selected reviews or an error message.
    """
    api_logger.info(f"POST request /reviews/select activated with body {query_input}")
    results = await run_in_threadpool(run_select_query, query_input)
    if results == "Error":
        api_logger.error(f"An error occurred selecting rows from table, see database.log for detail")
        raise HTTPException(status_code=400, detail="Unable to run select query, see database.log for details.")
    return JSONResponse(content=results, status_code=status.HTTP_200_OK)


@app.post("/reviews/insert")
async def insert_reviews_into_db(reviews: List[Review] = Body(...)):
    """
    Insert new reviews into the database.

    Example curl command:
    curl -X POST http://127.0.0.1:8000/reviews/insert \
         -H "Content-Type: application/json" \
         -d '[{"reviewer_name": "Danny Walters", ...}, {...}]'

    Args:
        reviews (List[Review]): A list of reviews to be inserted.

    Returns:
        JSONResponse: A response containing the IDs of the inserted reviews or an error message.
    """
    api_logger.info(f"POST request /reviews/insert activated with reviews {reviews}")
    inserted_ids = await run_in_threadpool(insert_reviews, reviews)
    if not inserted_ids:
        api_logger.error(f"An error occurred when trying to insert records into DB, see database.log")
        raise HTTPException(status_code=400, detail="Unable to insert rows, see log for details.")
    return JSONResponse(content={"inserted_ids": inserted_ids}, status_code=status.HTTP_201_CREATED)

@app.delete("/reviews/truncate")
async def delete_all_reviews_from_db():
    api_logger.info("Deleting all records in table")
    rows_deleted = await run_in_threadpool(delete_reviews)
    if rows_deleted == "Error":
        api_logger.error(f"Unable to delete records from DB, see database.log")
        raise HTTPException(status_code=400, detail="Unable to delete rows, see log for details.")
    return JSONResponse(content={"num_deleted_rows": rows_deleted}, status_code=status.HTTP_201_CREATED)


@app.delete("/reviews/delete")
async def delete_reviews_from_db(conditions: List[Condition] = Body(...)):
    """
    Delete reviews from the database based on specified conditions.

    Example curl command:
    curl -X DELETE http://127.0.0.1:8000/reviews/delete \
         -H "Content-Type: application/json" \
         -d '[{"column": "reviewer_name", "contains": "Danny"}]'

    Args:
        conditions (List[Condition]): Conditions to identify which reviews to delete.

    Returns:
        JSONResponse: A response indicating the number of rows deleted or an error message.
    """
    api_logger.info(f"DELETE request /reviews/select activated with conditions {conditions}")
    num_rows_deleted = await run_in_threadpool(delete_reviews, conditions)
    if not num_rows_deleted:
        api_logger.error(f"Unable to delete records from DB, see database.log")
        raise HTTPException(status_code=400, detail="Unable to delete rows, see log for details.")
    return JSONResponse(content={"num_deleted_rows": num_rows_deleted}, status_code=status.HTTP_201_CREATED)


@app.patch("/reviews/update")
async def update_reviews_in_db(conditions: List[Condition] = Body(...),
                               columns_to_update: List[ColumnToUpdate] = Body(...)):
    """
    Update reviews in the database based on specified conditions and update data.

    Example curl command:
    curl -X PATCH http://127.0.0.1:8000/reviews/update \
         -H "Content-Type: application/json" \
         -d '{"conditions": [{"column": "id", "equals": "1"}], "columns_to_update": [{"column_name": "review_title", "column_value": "Updated Title"}]}'

    Args:
        conditions (List[Condition]): Conditions to identify which reviews to update.
        columns_to_update (List[ColumnToUpdate]): Data for updating the reviews.

    Returns:
        JSONResponse: A response indicating the number of rows updated or an error message.
    """
    api_logger.info(f"PATCH request /reviews/update activated\n"
                    f"conditions: {conditions}"
                    f"columns_to_update: {columns_to_update}")
    num_updated_rows = await run_in_threadpool(update_review, conditions, columns_to_update)
    if not num_updated_rows:
        api_logger.error(f"Unable to update records in db from submitted params, see database.log for details")
        raise HTTPException(status_code=400, detail="Unable to update rows, see log for details.")
    return JSONResponse(content={"num_updated_rows": num_updated_rows}, status_code=status.HTTP_201_CREATED)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.routes.main:app", host="127.0.0.1", port=8000, reload=True)
