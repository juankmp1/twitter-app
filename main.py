from uuid import UUID
from datetime import date, datetime

from fastapi import FastAPI, status
from pydantic import BaseModel, EmailStr, Field
from typing import Optional,List

 
app = FastAPI()

#Models

class UserBase(BaseModel):
    pass

class UserLogin(UserBase):
    password : str =Field(
        ...,
        min_length = 8,
        max_length=64
    )

class User(UserBase):
    user_id:  UUID = Field(...) #universal unique identifier 
    email: EmailStr = Field(...)
    password : str =Field(
        ...,
        min_length = 8
    )
    first_name: str = Field(
        ...,
        min_length = 1,
        max_length = 50
    )
    birth_date: Optional[date] = Field(default= None)

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content : str = Field(
        ...,
        max_length=256,
        min_length=1
    )
    created_at : datetime = Field(default=datetime.now())
    update_at_time : Optional[datetime] = Field(default=None)
    by: User = Field(...)

#Path Operations


@app.get(
    path="/")
def home():
    return {
        "twitter API": "Working!"
    }

## Users

@app.post(
    path="/signup",
    response_model= User,
    status_code= status.HTTP_201_CREATED,
    summary="Register a user",
    tags=["Users"]
)
def signup():
    pass
@app.post(
    path="/signup",
    response_model= User,
    status_code= status.HTTP_201_CREATED,
    summary="Register a user",
    tags=["Users"]
)
def signup():
    pass

@app.post(
    path="/login",
    response_model= User,
    status_code= status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
)
def login():
    pass

@app.post(
    path="/users",
    response_model= User,
    status_code= status.HTTP_201_CREATED,
    summary="Register a user",
    tags=["Users"]
)
def signup():
    pass

@app.post(
    path="/signup",
    response_model= User,
    status_code= status.HTTP_201_CREATED,
    summary="Login a user",
    tags=["Users"]
)
def signup():
    pass

@app.get(
    path="/users",
    response_model= List[User],
    status_code= status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
)
def show_all_users():
    pass

@app.get(
    path="/users/{user_id}",
    response_model= User,
    status_code= status.HTTP_200_OK,
    summary="Show a User",
    tags=["Users"]
)
def show_a_user():
    pass

@app.delete(
    path="/users/{user_id}/delete",
    response_model= User,
    status_code= status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
)
def Delete_a_user():
    pass

@app.put(
    path="/users/{user_id}/update",
    response_model= User,
    status_code= status.HTTP_200_OK,
    summary="Update a User",
    tags=["Users"]
)
def update_a_user():
    pass
## Tweets
