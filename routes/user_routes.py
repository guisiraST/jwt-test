from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from auth.jwt_handler import create_access_token

from sqlmodel import select
from database.connection import get_session
from auth.hash_password import HashPassword
from auth.setting import TokenResponse, User, UserSignIn

user_router = APIRouter(
    tags=["User"]
)

users = {}
hash_password = HashPassword()

@user_router.post("/signup", status_code=201)
async def sign_new_user(user: User, session=Depends(get_session)) -> dict:
    statement = select(User).where(User.email == user.email)
    result = session.exec(statement)
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User supplied username exists"
        )
    else:
        hashed_password = hash_password.create_hash(user.password)
        user.password = hashed_password
        session.add(user)
        session.commit()
        session.refresh(user)

        return {
            "message": "User successfully registered!"
        }
#
@user_router.post("/signin", response_model=TokenResponse)
async def sign_user_in(user: OAuth2PasswordRequestForm = Depends(), session=Depends(get_session)) -> dict:
    statement = select(User).where(User.email == user.username)
    result = session.exec(statement)
    user_data = result.first()

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    if hash_password.verify_hash(user.password, user_data.password):
        access_token = create_access_token(user_data.email) #
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )
