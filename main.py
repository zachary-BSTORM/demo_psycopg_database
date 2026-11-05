from repository.users_repository import get_users_manual, create_user, delete_user
from db.db import Database


if __name__ == "__main__":
    continue_app = True

    while continue_app:
        try:
            print("Menu")
            print("Get all users - 1")
            print("Create new user - 2")
            print("Delete user - 3")
            print("Quit - 0")

            choice = input("Votre choix : ")

            match choice:
                case "1":
                    for v in get_users_manual():
                        print(v)
                case "2":
                    email = input("Entrez l'email : ")
                    last_name = input("Entrez le nom : ")
                    role = input("Entrez le role : ")
                    id = create_user(email, last_name, role)
                    print(f"l'utilisateur à bien été crée avec l'id {id}")

                case "3":
                    print("---------------------")
                    for v in get_users_manual():
                        print(v)
                    print("---------------------")
                    id = input("Entrez l'id de l'utilisateur à supprimer : ")
                    rows_count = delete_user(id)
                    print(f"{rows_count} lignes modifié")

                case "0":
                    continue_app = False
        except Exception as e :
            print(f"Erreur : {e}")
        