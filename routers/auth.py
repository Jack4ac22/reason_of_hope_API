# from db import models
from db.database import get_db
from fastapi import Depends, Response, status, APIRouter, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from utilities import hash_manager, jwt_manager
from db import db_user
from supabase import Client
router = APIRouter(
    prefix='/auth',
    tags=['authentication']
)

incorrectException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password ",
    headers={"WWW-Authenticate": "Bearer"}
)


@router.post('', status_code=status.HTTP_202_ACCEPTED)
def auth_user(user_credentials: OAuth2PasswordRequestForm = Depends(), db:Client = Depends(get_db)):

    corresponding_user = db_user.get_user_by_email(
        user_credentials.username, db)
    # print(corresponding_user)
    if not corresponding_user:
        raise incorrectException

    pass_valid = hash_manager.verify_password(
        user_credentials.password, corresponding_user['password'])

    if not pass_valid:
        raise incorrectException

    jwt = jwt_manager.generate_token(
        corresponding_user['id'], corresponding_user['email'], corresponding_user['activated'])
    return jwt
