from typing import List, Optional
from dao.db_connection import DBConnection
from utils.singleton import Singleton
from business_object.attack.abstract_attack import AbstractAttack
from business_object.attack.attack_factory import AttackFactory


class TypeAttackDAO(metaclass=Singleton):
    """
    Communicate with the attack_type table
    """

    def find_all_attack_type(self) -> List[str]:
        """
        Get all attack type names and return a list

        :return: A list of all types
        :rtype: List of str
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT *                                  "
                    "  FROM tp.attack_type                     "
                )

                # to store raw results
                res = cursor.fetchall()

        # Create an empty list to store formatted results
        type_attack: List[str] = []

        # if the SQL query returned results (ie. res not None)
        if res:
            for row in res:
                type_attack.append(row["attack_type_name"])

                print(row["id_attack_type"])
                print(row["attack_type_name"])
                print(row["attack_type_description"])

        return type_attack

    def find_id_by_label(self, label: str) -> Optional[int]:
        """
        Get the id_attack_type from the label
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id_attack_type                     "
                    "  FROM tp.attack_type                     "
                    " WHERE attack_type_name = %(attack_name)s ",
                    {"attack_name": label},
                )
                res = cursor.fetchone()

        if res:
            return res["id_attack_type"]

    def find_attack_by_id(self, id: int) -> Optional[AbstractAttack]:
        """
        Get an attack by its ID.

        :param id: The ID of the attack to find
        :return: An AbstractAttack instance or None if not found
        """
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id_attack_type, attack_name, attack_description "
                    "FROM tp.attack "
                    "WHERE id_attack_type = %(id)s",
                    {"id": id},
                )
                res = cursor.fetchone()

        if res:
            return AttackFactory().instantiate_attack(
                id=res["id_attack_type"],
                name=res["attack_name"],
                description=res["attack_description"],
            )
        return None


def find_all_attacks(
    self, limit: Optional[int] = None, offset: Optional[int] = None
) -> List[AbstractAttack]:
    """
    Get all attacks with optional pagination.

    :param limit: Maximum number of attacks to return
    :param offset: Number of attacks to skip before starting to collect the result set
    :return: A list of AbstractAttack instances
    """
    query = "SELECT id_attack, attack_name, attack_description FROM tp.attack"
    params = {}

    # Ajouter la pagination si limit ou offset sont spécifiés
    if limit is not None:
        query += " LIMIT %(limit)s"
        params["limit"] = limit
    if offset is not None:
        query += " OFFSET %(offset)s"
        params["offset"] = offset

    with DBConnection().connection as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            res = cursor.fetchall()

    # Convertir les résultats en instances de AbstractAttack
    attacks = []
    for row in res:
        attacks.append(
            AttackFactory().instantiate_attack(
                attack_id=row["id_attack_type"],
                name=row["attack_name"],
                description=row["attack_description"],
            )
        )

    return attacks


def update_attack(self, attack: AbstractAttack) -> bool:
    """
    Update the attack in the database.

    :param attack: An instance of AbstractAttack to update
    :return: True if the update was successful, False otherwise
    """
    query = """
        UPDATE tp.attack
        SET attack_name = %(name)s,
            attack_description = %(description)s
        WHERE id_attack_type = %(id)s
        """

    params = {
        "id": attack.id,
        "name": attack.name,
        "description": attack.description,
    }

    try:
        with DBConnection().connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                # Vérifier le nombre de lignes affectées
                if cursor.rowcount > 0:
                    return True
                else:
                    return False
    except Exception as e:
        print(f"An error occurred while updating the attack: {e}")
        return False


if __name__ == "__main__":
    # Pour charger les variables d'environnement contenues dans le fichier .env
    import dotenv

    dotenv.load_dotenv(override=True)

    attack_types = TypeAttackDAO().find_all_attack_type()
    print(attack_types)
