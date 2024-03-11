from fastapi import FastAPI, HTTPException, Response, status, Body
from starlette.concurrency import run_in_threadpool  # Allows synchronous code to run async by using threads
from fastapi.responses import JSONResponse
from typing import List

from app.crud.read import get_all_reviews, run_select_query
from app.crud.create import insert_reviews
from app.crud.delete import delete_reviews
from app.routes.routes_logger import api_logger
from app.models.models import QueryInput, Review, Condition


app = FastAPI()


# Example query
"""
curl -X GET http://127.0.0.1:8000/reviews/select \
     -H "Content-Type: application/json" \
     -d '{
           "table": "reviews",
           "columns": ["review_date", "reviewer_name"],
           "conditions": [
               {"column": "reviewer_name", "contains": "John"}
           ],
           "limit": "4"
         }'
"""
@app.get("/reviews/select")
async def run_query(query_input: QueryInput = Body(...)):
    api_logger.info(f"GET request /reviews/select activated with body {query_input}")
    results = await run_in_threadpool(run_select_query, query_input)
    if results == "Error":
        api_logger.error(f"An error occurred selecting rows from table, see database.log for detail")
        raise HTTPException(status_code=400, detail="Unable to run select query, see database.log for details.")
    return JSONResponse(content=results, status_code=status.HTTP_200_OK)


"""
curl -X POST http://127.0.0.1:8000/reviews/insert\
     -H "Content-Type: application/json" \
     -d '[{
            "reviewer_name": "Danny Walters", 
            "review_title": "Excellent Meal", 
            "review_rating": "5", 
            "review_content": "Good food", 
            "email_address": "dwdanielwalters@gmail.com", 
            "country": "United States", 
            "review_date": "2024-03-03"
            },
           {
            "reviewer_name": "Qanny Walters", 
            "review_title": "Excellent Meal", 
            "review_rating": "2", 
            "review_content": "Good food", 
            "email_address": "dwdanielwalters@gmail.com", 
            "country": "United Kingdom", 
            "review_date": "2024-03-03"
            }
            ]'
"""
@app.post("/reviews/insert")
async def insert_reviews_into_db(reviews : List[Review] = Body(...)):
    api_logger.info(f"POST request /reviews/insert activated with reviews {reviews}")
    inserted_ids = await run_in_threadpool(insert_reviews, reviews)
    if not inserted_ids:
        api_logger.error(f"An error occurred when trying to insert records into DB, see database.log")
        raise HTTPException(status_code=400, detail="Unable to insert rows, see log for details.")
    return JSONResponse(content={"inserted_ids": inserted_ids}, status_code=status.HTTP_201_CREATED)


"""
curl -X DELETE http://127.0.0.1:8000/reviews/delete \
    -H "Content-Type: application/json" \
     -d '[
               {"column": "reviewer_name", "contains": "Danny"}
        ]'
"""
@app.delete("/reviews/delete")
async def delete_reviews_from_db(conditions: List[Condition] = Body(...)):
    api_logger.info(f"DELETE request /reviews/select activated with conditions {conditions}")
    num_rows_deleted = await run_in_threadpool(delete_reviews, conditions)
    if not num_rows_deleted:
        api_logger.error(f"Unable to delete records from DB, see database.log")
        raise HTTPException(status_code=400, detail="Unable to delete rows, see log for details.")
    return JSONResponse(content={"num_deleted_rows": num_rows_deleted}, status_code=status.HTTP_201_CREATED)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.routes.main:app", host="127.0.0.1", port=8000, reload=True)
