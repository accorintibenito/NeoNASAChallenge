from datetime import date, datetime
from fastapi import FastAPI
from schemas import AsteroidsQueryParams, AsteroidItem, AsteroidsListResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello world"}


# @app.get("/api/v1/asteroids/{item_id}")
# async def asteroids(params: AsteroidsQueryParams):
#     return AsteroidsListResponse

