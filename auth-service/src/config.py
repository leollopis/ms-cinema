import os
from dotenv import load_dotenv

# Charger les variables d'environnement du fichier .env
load_dotenv()


# Classe de configuration Flask/Mongo
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    MONGO_INITDB_ROOT_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME")
    MONGO_INITDB_ROOT_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
    MONGO_DB = os.getenv("MONGO_DB")
    MONGO_USER = os.getenv("MONGO_USER")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
    MONGO_PORT = os.getenv("MONGO_PORT")
    MONGO_HOST = os.getenv("MONGO_HOST")
    # URI MongoDB pour Flask-PyMongo ou MongoClient
    MONGO_URI = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"

    # Config Mongo Express (optionnel)
    MONGO_EXPRESS_PORT = os.getenv("MONGO_EXPRESS_PORT")
    ME_CONFIG_MONGODB_ADMINUSERNAME = os.getenv("ME_CONFIG_MONGODB_ADMINUSERNAME")
    ME_CONFIG_MONGODB_ADMINPASSWORD = os.getenv("ME_CONFIG_MONGODB_ADMINPASSWORD")
    ME_CONFIG_MONGODB_SERVER = os.getenv("ME_CONFIG_MONGODB_SERVER")
