from fastapi import FastAPI
from starlette.concurrency import run_in_threadpool  # Allows synchronous code to run async by using threads

from app.crud.read import get_all_reviews
from app.crud.delete import delete_all_reviews

app = FastAPI()


# curl -X DELETE http://127.0.0.1:8000/reviews/delete
@app.delete("/reviews/delete")
async def remove_items():
    result = await run_in_threadpool(delete_all_reviews)
    return result


# curl -X GET http://127.0.0.1:8000/reviews/read
@app.get("/reviews/read")
async def read_items():
    result = await run_in_threadpool(get_all_reviews)
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.routes.main:app", host="127.0.0.1", port=8000, reload=True)
