from fastapi import APIRouter, Depends, status
from schemas import user_schemas
from db import db_user
from db.database import get_db
from utilities import jwt_manager
from supabase import Client


router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.post("",  status_code=status.HTTP_201_CREATED, response_model=user_schemas.UserDisplay)
def create_new_user(request: user_schemas.UserBase, db: Client = Depends(get_db)):
    db_user.create(request, db)
    return db_user.created_user(db)


@router.get("/all")
def get_all(db: Client = Depends(get_db)):
    return db.table('user').select('*').execute()


@router.get("/all_order")
def get_all(db: Client = Depends(get_db)):
    return db.table('user').select("id", "first_name", "last_name", "email",
                                   "created_at", "last_update", "activated", "verified").limit(1).order(id, desc=True).execute()
