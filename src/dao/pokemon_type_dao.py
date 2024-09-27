from typing import Optional
from dao.db_connection import DBConnection
from utils.singleton import Singleton

# from business_object.attack.abstract_attack import AbstractAttack
# from business_object.pokemon.pokemon_factory import PokemonFactory
# from business_object.attack.attack_factory import AttackFactory


class PokemonType(metaclass=Singleton):

    def find_pokemon_type(self, id_pokemon_type: int) -> Optional[str]:

        query = """
        SELECT pt.pokemon_type_name
        FROM tp.pokemon_type pt
        WHERE pt.id_pokemon_type = %(id_pokemon_type)s
        """
        params = {"id_pokemon_type": id_pokemon_type}

        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                res = cursor.fetchall()

        if res:
            pokemon_type = res[0]["pokemon_type_name"]

            return pokemon_type

        else:
            return None
