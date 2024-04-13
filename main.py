from dotenv import dotenv_values

from routes.routes import router as user_router

from contextlib import asynccontextmanager
from fastapi import FastAPI

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
db_uri = dotenv_values('.env')['DATABASE_URL']

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.mongo_client = MongoClient(db_uri, server_api=ServerApi('1'))
    app.database = app.mongo_client['comingBack']
    print("Connected to database")
    yield
    app.mongo_client.close()
    print("Disconnected from database")

app = FastAPI(lifespan=lifespan)

@app.get('/')
def index():
    return {"message": "Hello, World!"}

app.include_router(user_router, tags=["users"], prefix="/users")