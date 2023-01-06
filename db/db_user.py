from fastapi import HTTPException, status
import json
from supabase import Client
from schemas import user_schemas
from utilities import jwt_manager, hash_manager
from pydantic import EmailStr


def check_email_duplication(email: EmailStr, db: Client):
    usrs = db.table('user').select('email').execute()
    # print(usrs.data)
    for user in usrs.data:
        if user['email'] == email:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"{email} is already in use, please login or chose another email."
            )


def created_user(db: Client):
    created_user = db.table('user').select("id", "first_name", "last_name", "email", "created_at", "last_update", "activated", "verified").limit(1).order('id', desc=True).execute()
    # print(created_user)
    return created_user.data[0]


def create(request: user_schemas.UserBase, db: Client):
    new_user = {
        "first_name": request.first_name,
        "last_name": request.last_name,
        "email": request.email,
        "password": hash_manager.hash_pass(request.password),
    }
    check_email_duplication(request.email, db)
    db.table('user').insert(new_user).execute()
    return True
