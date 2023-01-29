#Python
from uuid import UUID
from datetime import date, datetime
import json
from typing import Optional,List

#Pydantic

from pydantic import BaseModel, EmailStr, Field

#FastAPI
from fastapi import FastAPI, status, Body
from fastapi.encoders import jsonable_encoder
 
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
    last_name: str = Field(
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

class UserRegister(User):
    password : str =Field(
        ...,
        min_length = 8,
        max_length=64
    )

# Path Operations


## Users

## Login a user
@app.post(
    path="/login",
    response_model= User,
    status_code= status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
)
def login():
    pass

## Register a user
@app.post(
    path="/signup",
    response_model= User,
    status_code= status.HTTP_201_CREATED,
    summary="Login a user",
    tags=["Users"]
)
def signup(user: UserRegister = Body(...)):
    """
    SingUp

    This path operation register a user in the app
    
    Parameters:
        - Request body parameter
            - user: UserRegister

    Returns a json with the basic user information:
        - user_id: UUID
        - email: EmailStr
        - firts_name: str
        - last_name: str
        - birth_date: date
    """
    with open("./users.json","r+", encoding="utf-8") as f:
        results = json.load(f)
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0) #para que no se genere mas listas en el archivo de users.js
        f.write(json.dumps(results))
        return user

### Show all users
@app.get(
    path="/users",
    response_model= List[User],
    status_code= status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
)
def show_all_users():
    pass

### Show a user
@app.get(
    path="/users/{user_id}",
    response_model= User,
    status_code= status.HTTP_200_OK,
    summary="Show a User",
    tags=["Users"]
)
def show_a_user():
    pass

### Delete a user
@app.delete(
    path="/users/{user_id}/delete",
    response_model= User,
    status_code= status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
)
def Delete_a_user():
    pass

### Update a user
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

### Show all tweets
@app.put(
    path="/",
    response_model= List[Tweet],
    status_code= status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweets"]
)
def Home():
    return {"Tweeter API":"Working!"}
    
### Post a tweet
@app.post(
    path="/post",
    response_model= Tweet,
    status_code= status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"]
)
def post():
    pass

### Show a tweet
@app.get(
    path="/tweets/{tweet_id}",
    response_model= Tweet,
    status_code= status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"]
)
def show_a_tweet():
    pass

### Delete a tweet
@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model= Tweet,
    status_code= status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
)
def delete_a_tweet():
    pass

### Delete a tweet
@app.put(
    path="/tweets/{tweet_id}/update",
    response_model= Tweet,
    status_code= status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"]
)
def delete_a_tweet():
    pass