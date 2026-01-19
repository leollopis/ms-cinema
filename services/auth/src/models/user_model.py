from bson import ObjectId
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

"""
Modèle utilisateur pour l'authentification. 
"""


class User(UserMixin):
    def __init__(self, user_data):
        """
        Définition d'un utilisateur.
        """
        self.id = str(user_data.get("_id"))
        self.email = user_data.get("email")
        self.password_hash = user_data.get("password")
        self.first_name = user_data.get("first_name")
        self.last_name = user_data.get("last_name")

    @staticmethod
    def get_by_id(collection, user_id):
        """
        Récupère un utilisateur par son ID.
        """
        try:
            data = collection.find_one({"_id": ObjectId(user_id)})
            if data:
                return User(data)
        except:
            return None
        return None

    @staticmethod
    def get_by_email(collection, email):
        """
        Récupère un utilisateur par son email.
        """
        data = collection.find_one({"email": email})
        if data:
            return User(data)
        return None

    @staticmethod
    def create(collection, email, password):
        """
        Crée un nouvel utilisateur.
        """
        from datetime import datetime, timezone

        hashed = generate_password_hash(password)
        now = datetime.now(timezone.utc)
        user_data = {
            "email": email,
            "password": hashed,
            "created_at": now,
            "updated_at": now,
        }
        res = collection.insert_one(user_data)
        user_data["_id"] = res.inserted_id
        return User(user_data)

    def check_password(self, password):
        """
        Vérifie si le mot de passe est correct.
        """
        return check_password_hash(self.password_hash, password)
