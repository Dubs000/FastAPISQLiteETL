from fastapi import FastAPI
from app.crud.read import get_all_reviews
from app.crud.delete import delete_all_reviews

app = FastAPI()


@app.get("/items/delete")
async def remove_items():
    data = delete_all_reviews()
    return data


@app.get("/items/read")
async def read_items():
    data = get_all_reviews()
    return data


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.routes.main:app", host="127.0.0.1", port=8000, reload=True)
