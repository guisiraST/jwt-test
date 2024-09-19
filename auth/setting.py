from sqlmodel import SQLModel, Field
from pydantic import  BaseModel, EmailStr


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: EmailStr
    password: str

    model_config = {
               "json_schema_extra" : {
            "example": {
                "email": "test1234@stelligence.com",
                "password": "strong123!!",
            }
        }
    }


class UserSignIn(SQLModel):
    email: EmailStr
    password: str

    model_config = {
               "json_schema_extra" : {
            "example": {
                "email": "test1234@stelligence.com",
                "password": "strong123!!",
            }
        }
    }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
