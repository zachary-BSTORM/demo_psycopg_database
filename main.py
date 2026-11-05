# Fonctions du repository : elles récupèrent elles-mêmes la connexion via le singleton,
# on n'a donc plus besoin de leur passer conn
from repository.users_repository import get_users, create_user, delete_user

# Importé mais pas utilisé ici pour l'instant : la connexion n'est jamais fermée explicitement.
# Pour la fermer en fin de programme : "with Database().connection:" autour de la boucle,
# ou Database().close() après la boucle
from db.db import Database


# Ce bloc ne s'exécute que si on lance ce fichier directement (python main.py),
# pas si un autre fichier l'importe
if __name__ == "__main__":
    # Fait tourner la boucle du menu ; passe à False pour quitter
    continue_app = True

    with Database().connection:
        while continue_app:
            # Le try est DANS la boucle : en cas d'erreur, on affiche le message
            # et le menu revient, au lieu d'arrêter le programme
            try:
                print("Menu")
                print("Get all users - 1")
                print("Create new user - 2")
                print("Delete user - 3")
                print("Quit - 0")

                # input() renvoie toujours une chaîne : on compare avec "1", pas avec 1
                choice = input("Votre choix : ")

                # match / case : équivalent d'une suite de if / elif (Python 3.10+)
                match choice:
                    case "1":
                        # Affiche chaque utilisateur (un tuple par ligne)
                        for v in get_users():
                            print(v)
                    case "2":
                        email = input("Entrez l'email : ")
                        last_name = input("Entrez le nom : ")
                        role = input("Entrez le role : ")
                        # create_user renvoie l'id généré par PostgreSQL (RETURNING id)
                        id = create_user(email, last_name, role)
                        print(f"l'utilisateur à bien été crée avec l'id {id}")

                    case "3":
                        # On affiche d'abord la liste pour voir les id disponibles
                        print("---------------------")
                        for v in get_users():
                            print(v)
                        print("---------------------")
                        id = input("Entrez l'id de l'utilisateur à supprimer : ")
                        # delete_user renvoie le nombre de lignes supprimées (0 ou 1)
                        rows_count = delete_user(id)
                        print(f"{rows_count} lignes modifié")

                    case "0":
                        # La condition du while devient fausse : la boucle s'arrête
                        continue_app = False
            # Attrape toutes les erreurs (base de données, saisie...) pour ne pas planter
            except Exception as e:
                print(f"Erreur : {e}")
