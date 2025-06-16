from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field
from typing import Optional, List
import datetime

app = FastAPI()

class Movie(BaseModel):
  id: int
  title: str
  overview: str
  year: int
  rating: Optional[float] = None
  category: str

  model_config = {
    'json_schema_extra': {
      'example': {
        'id': 1,
        'title': 'My movie',
        'overview': 'Esta pelicula es sobre ...',
        'year': 2022,
        'rating': 5, 
        'category': 'Accion'
      }
    }
  }

movies: List[Movie] = []

class MovieCreate(BaseModel):
  id: int = Field()
  title: str = Field(min_length=5, max_length=15, default='My Movie')
  overview: str = Field(min_length=15, max_length=55, default='Esta pelicua trata acerca de ...')
  year: int = Field(le=datetime.date.today().year, ge=1900)
  rating: float = Field(ge=0, le=10)
  category: str = Field(min_length=5, max_length=20)

class MovieUpdate(BaseModel):
  title: str
  overview: str
  year: int
  rating: Optional[float] = None
  category: str

@app.get('/movies', tags=['Home'])
def get_movies() -> List[Movie]:
  return [movie.model_dump() for movie in movies]

@app.get('/movies/{id}', tags=['Home'])
def get_movie(id: int = Path(gt=0)) -> Movie | dict:
  for movie in movies:
    if movie.id == id:
      return movie.model_dump()
  return {}

@app.get('/movies/', tags=['Home'])
def get_movie_by_category(category: str = Query(min_length=5, max_length=20)) -> Movie | dict:
  for movie in movies:
    if movie.category == category:
      return movie.model_dump()
    
  return {}
    

@app.post('/movies', tags=['Movies'])
def create_movie(movie: MovieCreate) -> List[Movie]:
  movies.append(movie)
  return [movie.model_dump() for movie in movies]

@app.patch('/movies/{id}', tags=['Movies'])
def update_movie(id: int, movie:MovieUpdate) -> List[MovieUpdate]:
  
  for item in movies:
    if item['id'] == id:
      item['title'] = movie.title
      item['overview'] = movie.overview
      item['year'] = movie.year
      item['rating'] = movie.rating
      item['category'] = movie.category
  return [movie.model_dump() for movie in movies]

@app.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id: int):
  for movie in movies:
    if movie['id'] == id:
      movies.remove(movie)
  return [movie.model_dump() for movie in movies]