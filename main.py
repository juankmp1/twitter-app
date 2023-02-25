#Python
from uuid import UUID
from datetime import date, datetime
import json 
from json import JSONEncoder, dumps
from typing import Optional,List
from jwt_manager import create_token, validate_token
from models.movie import Movie as MovieModel 
from config.database import Session, engine, Base
#Pydantic

from pydantic import BaseModel, EmailStr, Field

#FastAPI
from fastapi import FastAPI, status, Body, Depends, HTTPException, Path, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBearer


 
app = FastAPI()
app.title = "Mi aplicación con fastAPI"
app.version = "0.0.1"

#Models

Base.metadata.create_all(bind = engine)

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail = "Credenciales son invalidas")

class UserBase(BaseModel):
    email: str
    password: str

class Movie(BaseModel):
    id : Optional[int] = None
    title : str = Field(min_length=15, max_length=50)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)
    rating : float= Field(ge=1, le=10)
    category : str = Field(min_length=5, max_length=15)

    class Config: 
        schema_extra = {
            "example": {
                "id": 1,
                "title":"My movie",
                "overview": "Movie's description",
                "year": 2022,
                "rating":9.8,
                "category": "Action"
            }
        }

movies = [
    {
		"id": 1,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	},
    {
		"id": 2,
		"title": "Avatar",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Acción"
	}
]    

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
        min_length = 5
    )
    # first_name: str = Field(
    #     ...,
    #     min_length = 1,
    #     max_length = 50
    # )
    # last_name: str = Field(
    #     ...,
    #     min_length = 1,
    #     max_length = 50
    # )
    #birth_date: Optional[date] = Field(default= None)

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
@app.get(
    path='/', 
    tags=['home'])
def message():
    return HTMLResponse('<h1> Hello World</h1>')

## Users

## Login a user
@app.post(
    path="/login",
    response_model= User,
    status_code= status.HTTP_200_OK,
    summary="Login a User",
    tags=["auth"]
)
def login(user:User):
    if user.email == "admin@gmail.com" and user.password =="admin":
        token : str = create_token(user.dict())
        return JSONResponse(status_code=200, content=JSONEncoder.default(token))

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

##movies

@app.get(
    path='/movies',
    tags=['movies'],
    response_model = List[Movie], 
    status_code = 200,
    dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@app.get(
    path='/movies/{id}',
    tags = 'movies',
    response_model=Movie)
def get_movie(id:int = Path(ge=1, le=2000))->Movie:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content = {'message': 'No encontrado'})
    return JSONResponse(status_code = 200, content= jsonable_encoder(result))
        

@app.get(
    path='/movies/', 
    tags= ['movies'],
    response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    data = [item for item in movies if item ['category']== category]
    return JSONResponse(content = data)

@app.post(
    path='/movies',
    tags= ['movies'],
    response_model= dict,
    status_code=201)
def create_movie(movie:Movie)-> dict:
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201, content={"message":"The movie has registered"})

@app.put(
    path='/movies/{id}',
    tags= ['movies'],
    response_model=dict,
    status_code=200)
def update_movie(id: int, movie:Movie)-> dict:
    for item in movies: 
        if item ["id"] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            return JSONResponse(status_code=200, content={"message":"The movie has been update"})

@app.delete(
    path='/movies/{id}',
    tags=['movies'], 
    response_model=dict,
    status_code=200)
def delete_movie(id:int)-> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(status_code=200, content={"message": "The movie has been delete"})
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