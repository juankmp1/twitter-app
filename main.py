from uuid import UUID
from datetime import date, datetime

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

 
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

@app.get(
    path="/")
def home():
    return {
        "twitter API": "Working!"
    }