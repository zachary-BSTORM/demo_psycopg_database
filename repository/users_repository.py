"""Requêtes SQL sur la table users.

Récap des méthodes psycopg utilisées
------------------------------------
Connexion (Database().connection)
    conn.cursor()       crée un curseur, l'objet qui exécute les requêtes et lit les résultats
    conn.commit()       valide la transaction : les modifications sont enregistrées en base
    conn.rollback()     annule tout ce qui a été fait depuis le dernier commit
    conn.close()        ferme la connexion
    Avec autocommit=True (voir db.py), chaque requête est validée tout de suite :
    commit() et rollback() n'ont alors rien à valider ou à annuler.

Curseur
    cursor.execute(sql, params)   envoie une requête. Les valeurs vont dans un tuple à part
                                  et remplacent les %s : psycopg les sécurise (pas d'injection SQL).
                                  Pour une seule valeur, le tuple s'écrit (id,), avec la virgule.
    cursor.fetchall()   récupère toutes les lignes du résultat : liste de tuples
                        [(1, "a@b.fr", "Dupont", "admin"), ...], ou [] si aucune ligne
    cursor.fetchone()   récupère la ligne suivante : un tuple, ou None s'il n'y en a plus
    cursor.fetchmany(n) récupère les n lignes suivantes : liste de tuples
    cursor.rowcount     nombre de lignes touchées par la dernière requête (INSERT, UPDATE, DELETE)
    cursor.close()      ferme le curseur

Gestion avec "with"
    with conn.cursor() as cursor:   ferme le CURSEUR à la fin du bloc (pas la connexion)
    with conn:                      ferme la CONNEXION à la fin du bloc (psycopg 3), avec
                                    commit si tout s'est bien passé, rollback en cas d'erreur

Erreurs
    psycopg.Error       classe de base de toutes les erreurs psycopg
    e.sqlstate          code d'erreur PostgreSQL, par exemple "42P01" pour une table inexistante
    e.diag.message_primary   message d'erreur principal renvoyé par PostgreSQL
"""

from psycopg import Error  # classe de base des erreurs psycopg
from db.db import Database  # singleton qui fournit la connexion unique


def get_users():
    # Database() renvoie l'instance unique, .connection la connexion partagée.
    # Le with ferme automatiquement le CURSEUR à la fin du bloc ;
    # la connexion, elle, reste ouverte pour les autres fonctions.
    with Database().connection.cursor() as cursor:
        cursor.execute("SELECT * FROM users")

        # fetchall() : récupère toutes les lignes, sous forme de liste de tuples
        users = cursor.fetchall()

        return users


def create_user(email, last_name, role):
    with Database().connection.cursor() as cursor:
        # Les %s sont remplacés par les valeurs du tuple, dans l'ordre.
        # RETURNING id : PostgreSQL renvoie l'id généré pour la nouvelle ligne
        cursor.execute(
            """
                       INSERT INTO users (email,last_name,role)
                       VALUES (%s,%s,%s)
                       RETURNING id
                       """,
            (email, last_name, role),
        )
        # fetchone() : récupère une seule ligne, ici un tuple comme (12,)
        user_id = cursor.fetchone()[0]  # [0] : première valeur du tuple, l'id
        return user_id


def delete_user(id):
    with Database().connection.cursor() as cursor:
        # (id,) : tuple d'un seul élément, la virgule est obligatoire
        cursor.execute("DELETE FROM users WHERE id = %s", (id,))

        # rowcount : nombre de lignes supprimées (1 si l'id existait, 0 sinon)
        rows_count = cursor.rowcount

        return rows_count


# ---------------------------------------------------------------------------
# Gestion manuelle du curseur et de la connexion (sans with), pour comparaison
# ---------------------------------------------------------------------------

# Récupère l'instance unique de Database (la même que partout ailleurs)
db = Database()


def get_users_manual():
    try:
        # Initialisées à None pour pouvoir les tester dans le except et le finally,
        # même si une erreur survient avant leur création
        conn = None
        cursor = None

        # Récupération de la connexion partagée via l'instance de Database
        conn = db.connection

        # Ouverture manuelle du curseur
        cursor = conn.cursor()

        # Nom de table volontairement faux, pour déclencher une erreur et tester le except
        cursor.execute("SELECT * FROM qsdkjlqsdlf")

        users = cursor.fetchall()

        # Commit manuel (sans effet ici, puisque la connexion est en autocommit)
        conn.commit()
    except Error as e:
        # Exécuté seulement si une erreur psycopg survient dans le try
        if conn is not None:
            # Rollback manuel : annule la transaction en cours
            conn.rollback()
            # On relance une erreur plus lisible, avec le code et le message de PostgreSQL
            raise Exception(f"erreur : {e.sqlstate} - {e.diag.message_primary}")
    else:
        # Exécuté seulement s'il n'y a eu aucune erreur dans le try
        return users
    finally:
        # Toujours exécuté, en dernier, erreur ou pas
        print("finally")
        if cursor is not None:
            # Attention : ce code ferme la CONNEXION partagée, pas le curseur.
            # Le curseur reste ouvert, et la connexion du singleton est fermée pour tout le
            # programme (elle sera rouverte au prochain accès à db.connection).
            # Pour fermer seulement le curseur : cursor.close()
            cursor.close()
