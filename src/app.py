from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from dao.pokemon_dao import PokemonDAO

app = FastAPI()


@app.get("/hello")
async def get_hello():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def get_hello_name(name: str):
    return {"message": "Hello {}".format(name)}


# Define a Pydantic model for the character
class Personnage(BaseModel):
    nom: str
    age: int


# Create a dictionary to store characters
characters_db: Dict[int, Personnage] = {}
characters_db[1] = Personnage(nom="Anne", age=33)
characters_db[2] = Personnage(nom="Michel", age=20)
character_id = 3  # Initial character ID


# List all characters
@app.get("/character/")
def list_characters():
    return characters_db


# Add a character
@app.post("/character/")
def create_character(character: Personnage):
    global character_id
    characters_db[character_id] = character
    character_id += 1
    return character


# Update a character by ID
@app.put("/character/{character_id}")
def update_character(character_id: int, character: Personnage):
    if character_id not in characters_db:
        raise HTTPException(status_code=404, detail="Character not found")
    characters_db[character_id] = character
    return character


# Delete a character by ID
@app.delete("/character/{character_id}")
def delete_character(character_id: int):
    if character_id not in characters_db:
        raise HTTPException(status_code=404, detail="Character not found")
    deleted_character = characters_db.pop(character_id)
    return deleted_character


# Défintion du endpoint get /pokemon`/{name}
@app.get("/pokemon/{name}")
async def get_pokemon_by_name(name: str):
    pokemon = PokemonDAO().find_pokemon_by_name(name)
    if pokemon is None:
        # Si le Pokémon n'est pas trouvé, lever une exception HTTP 404
        raise HTTPException(status_code=404, detail="Pokémon non trouvé")
    return pokemon


# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80)


# # Défintion du endpoint get /attack?limit=100
# @app.get("/attack/")
# async def get_all_attacks(limit: int):
#     # TODO: récupérer les attaques en base en utilisant votre DAO
#     return attacks


# # Défintion du endpoint get /pokemon?limit=100
# @app.get("/pokemon/")
# async def get_all_pokemons(limit: int):
#     # TODO: récupérer les pokemons en base en utilisant votre DAO
#     return pokemons
