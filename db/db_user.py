from fastapi import HTTPException, status
import json
from time import time

from supabase import Client
from schemas import user_schemas
from utilities import jwt_manager, hash_manager, email_manager
from pydantic import EmailStr
from config import settings

##########################
##### checking methods####
##########################


def check_email_duplication(email: EmailStr, db: Client):
    user = db.table('user').select('email').eq("email", email).execute()
    print(user.data)

    if user.data[0]['email']:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{email} is already in use, please login or chose another email.")


def get_user_by_email(email: EmailStr, db: Client):
    user = db.table('user').select('email', 'password',
                                   'id', 'activated', 'verified', 'admin','token').eq("email", email).execute()
    return user.data[0]

##########################
##### router' methods#####
##########################


def created_user(db: Client):
    created_user = db.table('user').select("id", "first_name", "last_name", "email", "created_at",
                                           "last_update", "activated", "verified").limit(1).order('id', desc=True).execute()
    # print(created_user)
    return created_user.data[0]


def create(request: user_schemas.UserBase, db: Client):
    generated_token = jwt_manager.generate_validation_token(
        time(), request.email, "ActivateMyAccount", 360)
    new_user = {
        "first_name": request.first_name,
        "last_name": request.last_name,
        "email": request.email.lower(),
        "password": hash_manager.hash_pass(request.password),
        "token": generated_token
    }
    check_email_duplication(request.email, db)
    db.table('user').insert(new_user).execute()
    email_manager.send_email_with_subject("API regestration.", request.email, "Verfication link", f"""Hello {request.first_name} {request.last_name},
    Please use the following link to verify your account
    {settings.host_name}/user/activate/{generated_token}
    This token is valid for 24 hrs only.
    Thank you.""")
    return True


def validate_email_address_for_new_user(token: str, db: Client):
    decoded_email = jwt_manager.decode_token_email_validation(token)
    targeted_user = get_user_by_email(decoded_email, db)
    print(targeted_user)
    if targeted_user['token'] != token:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="The token is already used. please request a new token or contact support."
        )
    else:

        data = db.table("user").update(
            {"verified": True, "activated": True, "token": None}).eq("id", targeted_user['id']).execute()
        return data


def get_all(db: Client):
    return db.table('user').select("id", "first_name", "last_name", "email",
                                   "created_at", "last_update", "activated", "verified").execute().data
