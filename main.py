from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse



app = FastAPI()

@app.get("/")
def say_hello():
    return FileResponse("mini-frontend/hello.html")


@app.get("/readme")
def give_readme():
    return FileResponse("mini-frontend/readme.md")


catalog = [
    {
        "id": 1,
        "title": "Немо",
        "genre": "Развивающие",
        "players": 5
    },
    {
        "id": 2,
        "title": "Лото",
        "genre": "Русские-народные",
        "players": 10
    },
    {
        "id": 3,
        "title": "Домино",
        "genre": "Русские-народные",
        "players": 3
    },
    {
        "id": 4,
        "title": "Настольный теннис",
        "genre": "Европейские",
        "players": 2
    }
]
##начало самой интересной части

#классы обработки
class Games(BaseModel):
    id: int
    title: str
    genre: str
    players: int

class CreateGame(BaseModel):
    title: str
    genre: str
    players: int

#Самая оегкая часть кода : GET
@app.get("/games", response_model=list[Games])
def return_games():
    return catalog

#ПОСТ ЗАПРОС
@app.post("/games", response_model=Games, status_code=201)
def create_game(game: CreateGame):
    game_id = len(catalog) + 1
    new_game = {
        "id": game_id,
        "title": game.title,
        "genre": game.genre,
        "players": game.players
    }
    catalog.append(new_game)
    return new_game

#пут
#(надеюсь так написать можно просто  пут запрос выражать так мне намного легче)

@app.put("/games/{game_id}", response_model=Games)
def uptade_game(game_id: int, game: CreateGame):
    for saved_game in catalog:
        if saved_game["id"] == game_id:
            saved_game["id"] = game_id
            saved_game["title"] = game.title
            saved_game["genre"] = game.genre
            saved_game["players"] = game.players

#удаление

@app.delete("/games/{game_id}", response_model=list[Games])
def delete_game(game_id: int):
    for index, game_to_delete in enumerate(catalog):
        if game_to_delete["id"] == game_id:
            we_deleting_this = catalog.pop(index)
            return we_deleting_this