from psycopg import Connection
import psycopg
from db.db import Database

# def get_all_users(conn : "Connection"):
#     try:
#         cursor = conn.cursor()

#         cursor.execute("SELECT * FROM users")
#         users = cursor.fetchall()

#         conn.commit()
#     except:
#         conn.rollback()

#     else:
#         return users

#     finally:
#         if cursor is not None:
#             conn.close()

db = Database()  # permet de fermer la connection


def get_users():
    with Database().connection.cursor() as cursor:  # donne accès à la connection
        cursor.execute("SELECT * FROM users")

        users = cursor.fetchall()

        return users


def create_user(email, last_name, role):
    with Database().connection.cursor() as cursor:
        cursor.execute(
            """
                       INSERT INTO users (email,last_name,role)
                       VALUES (%s,%s,%s)
                       RETURNING id                       
                       """,
            (email, last_name, role),
        )
        user_id = cursor.fetchone()[0]
        return user_id


def delete_user(id):
    with Database().connection.cursor() as cursor:
        cursor.execute("DELETE FROM users WHERE id = %s", (id,))

        rows_count = cursor.rowcount

        return rows_count


def get_users_manual():
    try:
        conn = None
        cursor = None

        conn = db.connection

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM qsdkjlqsdlf")

        users = cursor.fetchall()

        conn.commit()
    except psycopg.Error as e:
        if conn is not None:
            conn.rollback()
            raise Exception(f"erreur : {e.sqlstate} - {e.diag.message_primary}")
    else:
        return users
    finally:
        print("finally")
        if cursor is not None:
            conn.close()
