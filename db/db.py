import psycopg  # librairie qui communique avec PostgreSQL (version 3)
from dotenv import load_dotenv  # lit le fichier .env
import os  # os.getenv() lit les variables d'environnement

# Charge les lignes du fichier .env (DB_NAME=..., etc.) dans les variables d'environnement.
# Exécuté une seule fois, au premier import de ce module.
load_dotenv()


class Database:
    """Singleton : une seule instance de Database existe dans tout le programme,
    donc une seule connexion à la base est partagée par tous les fichiers."""

    # Attribut de classe, partagé par toutes les instances :
    # il garde l'unique instance (None tant qu'elle n'a pas été créée)
    _instance = None

    # __new__ est exécuté avant __init__, au moment où on écrit Database().
    # C'est lui qui fabrique l'objet : en le redéfinissant, on renvoie toujours
    # le même objet au lieu d'en créer un nouveau à chaque appel.
    def __new__(cls):
        if cls._instance is None:
            # Premier appel : on crée l'objet, une seule fois
            cls._instance = super().__new__(cls)
            # La connexion n'est pas encore ouverte : elle le sera au premier
            # accès à .connection (voir plus bas)
            cls._instance._connection = None

        # Premier appel ou centième : c'est toujours la même instance
        # (Database() is Database() vaut True)
        return cls._instance

    # @property permet d'écrire Database().connection, sans parenthèses,
    # comme un attribut, alors qu'une méthode s'exécute derrière
    @property
    def connection(self):
        # On ouvre une connexion s'il n'y en a pas encore,
        # ou si la précédente a été fermée
        if self._connection is None or self._connection.closed:
            # Les informations de connexion viennent du fichier .env
            # (jamais écrites en dur dans le code)
            self._connection = psycopg.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                # autocommit=True : chaque requête est validée immédiatement,
                # pas besoin d'appeler commit()
                autocommit=True,
            )

        # On renvoie la connexion unique (déjà ouverte ou qu'on vient d'ouvrir)
        return self._connection

    # Ferme la connexion manuellement, à appeler une seule fois en fin de programme
    def close(self):
        # On ne ferme que si une connexion existe et est encore ouverte
        if self._connection is not None and not self._connection.closed:
            self._connection.close()

        # On oublie la connexion : un prochain accès à .connection en rouvrira une neuve
        self._connection = None
