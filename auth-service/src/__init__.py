from datetime import timedelta
from flask import Flask, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    verify_jwt_in_request,
)
from flask_login import LoginManager
from pymongo import MongoClient
import pymongo
from .config import Config

# Initialisation des extensions sans les lier tout de suite
login_manager = LoginManager()
mongo_client = MongoClient()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 1. Configuration base de données
    client = MongoClient(app.config["MONGO_URI"])
    app.db = client.get_default_database()

    # Permettre de stocker les JWT révoqués & supprimer automatiquement après expiration
    try:
        app.db.jwt_blocklist.create_index([("jti", pymongo.ASCENDING)], unique=True)
    except Exception:
        pass
    try:
        app.db.jwt_blocklist.create_index("expires_at", expireAfterSeconds=0)
    except Exception:
        pass

    # 2. Setup Flask-Login
    login_manager.init_app(app)

    # Désactiver la redirection HTML par défaut de Flask-Login
    @login_manager.unauthorized_handler
    def unauthorized():
        return (
            jsonify({"error": "Unauthorized", "message": "Authentification requise."}),
            401,
        )

    # 3. Setup JWT
    app.config.setdefault("JWT_SECRET_KEY", app.config.get("SECRET_KEY"))
    app.config.setdefault("JWT_ACCESS_TOKEN_EXPIRES", timedelta(minutes=60))

    jwt = JWTManager()
    jwt.init_app(app)

    # Blacklist des tokens (revocation)
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload.get("jti")
        if not jti:
            return False
        return bool(app.db.jwt_blocklist.find_one({"jti": jti}))

    # Prolongation automatique du JWT : si une requête contient un JWT valide
    @app.after_request
    def refresh_jwt(response):
        try:
            # optional=True évite d'élever une erreur si aucun token n'est fourni
            verify_jwt_in_request(optional=True)
        except Exception:
            # token absent ou invalide -> on ne fait rien
            return response

        identity = get_jwt_identity()
        if identity:
            # créer un nouveau token et l'envoyer dans l'en-tête de réponse
            new_token = create_access_token(identity=identity)
            response.headers["X-Access-Token"] = new_token

        return response

    # 4. Import et Enregistrement des Blueprints (Routes)
    from src.routes.auth_routes import auth_bp
    
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
