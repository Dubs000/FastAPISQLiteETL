from fastapi import FastAPI, HTTPException, Body
from starlette.concurrency import run_in_threadpool  # Allows synchronous code to run async by using threads

from app.crud.read import get_all_reviews, run_select_query
from app.crud.delete import delete_all_reviews
from app.routes.routes_logger import api_logger
from app.models.models import QueryInput


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
           ]
         }'
"""

# curl -X GET http://127.0.0.1:8000/reviews/select
@app.get("/reviews/select")
async def run_query(query_input: QueryInput = Body(...)):
    try:
        results = run_select_query(query_input)
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# curl -X DELETE http://127.0.0.1:8000/reviews/delete
@app.delete("/reviews/delete")
async def remove_items():
    api_logger.info(f"/reviews/delete triggered")
    result = await run_in_threadpool(delete_all_reviews)
    return result


# curl -X GET http://127.0.0.1:8000/reviews/read
@app.get("/reviews/read")
async def read_items():
    api_logger.info(f"/reviews/read triggered")
    result = await run_in_threadpool(get_all_reviews)
    api_logger.info(f"Result: {result}")
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.routes.main:app", host="127.0.0.1", port=8000, reload=True)
