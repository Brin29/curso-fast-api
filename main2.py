from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Movie(BaseModel):
  id: int | None = None
  title: str
  overview: str
  year: int
  rating: float
  category: str

movies = [
  {
    "id": 1,
    "title": "Avatar",
    "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
    "year": 2009,
    "rating": 7.8,
    "category": "Accion"
  }
]

@app.post('/movies', tags=['Movies'])
def create_movie(movie: Movie):
  movies.append(movie.model_dump())
  return movies