from fastapi import FastAPI
from routes.user import router as user_router
from routes.auth import router as auth_router
from database.connection import engine, Base
from database import models
from dotenv import load_dotenv


app = FastAPI()

load_dotenv()
Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(auth_router)


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}
