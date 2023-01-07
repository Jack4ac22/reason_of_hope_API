from fastapi import FastAPI
from pydantic import BaseModel
from db.database import supabase
from routers import auth, user
# from flask import Flask

# app = Flask(__name__)


# @app.route('/', methods=["GET"])
# def hello_world():
#     return "Hello World"


app = FastAPI()


@app.get("/")
def rout():
    return "Hello world"


app.include_router(auth.router)
app.include_router(user.router)

# @app.get("/users")
# def users():
#     users = supabase.table('user').select('*').execute()
#     return users


# @app.get("/")
# def root():
#     return {"message": "Test - Hello World"}


# @app.post("/user")
# def add_user():
#     supabase.table('user').insert({}).execute()
