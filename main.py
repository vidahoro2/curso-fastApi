from fastapi import FastAPI,Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title = "Mi aplicación con fastApi"
app.version = "0.0.1"


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=3, max_length=10)

    model_config = {
     "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "Mi Pelicula",
                    "overview": "Descripcion de la pelicula",
                    "year": 2022,
                    "rating": 9.9,
                    "category": "Acción"
                }
            ]
        }
    }

movies = [
    {
        "id":1,
        "title": "Avatar",
        "overview": "En un planeta llamado",
        "year": "2009",
        "rating": 7.8,
        "category": "Action"

    },
    {
        "id":2,
        "title": "Chuqui",
        "overview": "En un planeta llamado",
        "year": "2009",
        "rating": 7.8,
        "category": "Horror"

    },
    {
        "id":3,
        "title": "Avatar",
        "overview": "En un planeta llamado",
        "year": "2009",
        "rating": 7.8,
        "category": "Horror"
    }
    
]

@app.get('/', tags=['homepage'])
def message():
    return HTMLResponse('<h1>Hello</h1>')


@app.get('/movies', tags=['movies'],response_model=List[Movie], status_code=200)
def get_movies()->List[Movie]:
    return JSONResponse(status_code=200, content=[movies])

@app.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id:int = Path(ge=1, le=2000))->Movie:
    for item in movies:
        if item["id"]  == id:
            return JSONResponse(content=item)
        else:
            return JSONResponse(status_code=404, content=[])
    

# @app.get('/movies/',tags=['movies-category'])
# def get_movies_by_category(category: str, year:int):
#     return category

@app.get('/movies/', tags=['movies'],response_model=List[Movie])
def get_movie_using_category(category:str = Query(min_length=5, max_length=15))->List[Movie]:
    movie_list = []
    for item in movies:
        if item["category"] == category:
            movie_list.append(item)
        else:
            return JSONResponse(status_code=404, content={"message":"No se ha encontrado la cagegoria"})
    return movie_list

@app.post('/movies', tags=['movies'], response_model=dict,status_code=201)
def create_movie(movie: Movie)->dict:
    movies.append(movie)
    return  JSONResponse(status_code=201, content={"message":"Se ha añadido la pelicula "})

@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id:int, movie: Movie)->dict:
    for item in movies :
        if item["id"] == id:
            item['title']= movie.title
            item['overview']= movie.overview
            item['year']= movie.year
            item['rating']= movie.rating
            item['category']= movie.category
            return  JSONResponse(status_code=200, content={"message":"Se ha modificado la pelicula "})
        

@app.delete('/movies/{id}', tags=['movies'], response_model=dict)
def delete_movie(id:int)->dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return  JSONResponse(content={"message":"Se ha eliminado la pelicula "})






    