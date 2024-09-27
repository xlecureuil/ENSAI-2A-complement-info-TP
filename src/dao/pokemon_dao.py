from typing import List, Optional
from dao.db_connection import DBConnection
from utils.singleton import Singleton
from business_object.pokemon.abstract_pokemon import AbstractPokemon
from business_object.attack.abstract_attack import AbstractAttack
from business_object.pokemon.pokemon_factory import PokemonFactory
from business_object.attack.attack_factory import AttackFactory


class PokemonDAO(metaclass=Singleton):

    def find_all_pokemon(self) -> List[AbstractPokemon]:
        """
        Get all Pokémon from the database.

        :return: A list of AbstractPokemon instances
        """
        query = """'
        SELECT id_pokemon_type, name
        FROM tp.pokemon
        """

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                res = cursor.fetchall()

        # Convertir les résultats en instances de AbstractPokemon
        pokemons = []
        for row in res:
            pokemons.append(
                AbstractPokemon(pokemon_id=row["id_pokemon_type"], name=row["name"])
            )

        return pokemons

    def find_pokemon_by_name(self, name: str) -> Optional[AbstractPokemon]:
        """
        Get a Pokémon by its name along with its attacks.

        :param name: The name of the Pokémon to find
        :return: An instance of AbstractPokemon or None if not found
        """
        query = """
        SELECT p.id_pokemon_type, p.name,
               a.id_attack_type, a.attack_name, a.attack_description
        FROM tp.pokemon p
        LEFT JOIN tp.pokemon_attack pa ON p.id_pokemon_type = pa.id_pokemon
        LEFT JOIN tp.attack a ON pa.id_attack = a.id_attack_type
        WHERE p.name = %(name)s
        """

        params = {"name": name}

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                res = cursor.fetchall()

        if res:
            # Création d'un Pokémon et de sa liste d'attaques
            attacks = []
            pokemon_id = res[0]["id_pokemon_type"]
            pokemon_name = res[0]["name"]

            for row in res:
                if row["id_attack"]:  # Si une attaque est trouvée
                    attacks.append(
                        AttackFactory().instantiate_attack(
                            id=row["id_attack_type"],
                            name=row["attack_name"],
                            description=row["attack_description"],
                        )
                    )

            return AbstractPokemon(id=pokemon_id, name=pokemon_name, attacks=attacks)
        return None
