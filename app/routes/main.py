from fastapi import FastAPI, HTTPException, Response, status, Body
from starlette.concurrency import run_in_threadpool  # Allows synchronous code to run async by using threads
from fastapi.responses import JSONResponse
from typing import List

from app.crud.read import get_all_reviews, run_select_query
from app.crud.create import insert_reviews
from app.crud.delete import delete_all_reviews
from app.routes.routes_logger import api_logger
from app.models.models import QueryInput, Review


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
    results = await run_in_threadpool(run_select_query, query_input)
    if results == "Error":
        raise HTTPException(status_code=400, detail="Unable to run select query, see log for details.")
    return JSONResponse(content=results, status_code=status.HTTP_200_OK)


# curl -X GET http://127.0.0.1:8000/reviews/read
@app.get("/reviews/read")
async def read_items():
    results = await run_in_threadpool(get_all_reviews)
    if results == "Error":
        raise HTTPException(status_code=400, detail="Unable to run select query, see log for details.")
    return JSONResponse(content=results, status_code=status.HTTP_200_OK)


# curl -X DELETE http://127.0.0.1:8000/reviews/delete
@app.delete("/reviews/delete")
async def remove_items():
    api_logger.info(f"/reviews/delete triggered")
    result = await run_in_threadpool(delete_all_reviews)
    return result

"""
curl -X PATCH http://127.0.0.1:8000/reviews/insert\
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
@app.patch("/reviews/insert")
async def insert_reviews_into_db(reviews : List[Review] = Body(...)):
    inserted_ids = await run_in_threadpool(insert_reviews, reviews)
    if not inserted_ids:
        raise HTTPException(status_code=400, detail="Unable to insert rows, see log for details.")
    return JSONResponse(content={"inserted_ids": inserted_ids}, status_code=status.HTTP_201_CREATED)  # Changed status code to 201


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.routes.main:app", host="127.0.0.1", port=8000, reload=True)
