from fastapi import FastAPI
from pydantic import BaseModel
from db.database import supabase
from routers import auth, user
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


@app.get("/")
def rout():
    return "Hello world"


app.include_router(auth.router)
app.include_router(user.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=['*']
)
