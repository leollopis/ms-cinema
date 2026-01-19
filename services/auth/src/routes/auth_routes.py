from bson import ObjectId
from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import (
    create_access_token,
    decode_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from flask_login import logout_user
from src.models.user_model import User
from src.services.validation_service import (
    validate_user_login,
    validate_user_register,
    validate_user_update_profile,
)
from src.services.user_service import serialize_user, update_last_login
from src.services.auth_utils import revoke_token
from datetime import datetime

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    # 1. Validation
    is_valid, error_response = validate_user_register(data)
    if not is_valid:
        return jsonify(error_response), 400

    users_col = current_app.db.users

    # 2. Vérification d'unicité
    if User.get_by_email(users_col, data["email"]):
        return jsonify({"error": "Email déjà pris"}), 409

    # 3. Création de l'utilisateur
    try:
        new_user = User.create(users_col, data["email"], data["password"])
        return jsonify({"message": "Compte créé", "id": new_user.id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    # Valider le payload
    is_valid, error_response = validate_user_login(data)
    if not is_valid:
        return jsonify(error_response), 400

    users_col = current_app.db.users

    user = User.get_by_email(users_col, data.get("email"))

    if user and user.check_password(data.get("password")):
        try:
            update_last_login(current_app.db.users, user.id)
        except Exception:
            pass

        # Génère un JWT
        access_token = create_access_token(identity=user.id)
        return (
            jsonify({"message": "Connecté avec succès", "access_token": access_token}),
            200,
        )

    return jsonify({"error": "Identifiants invalides"}), 401


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    # Révoque le token JWT via le helper
    try:
        revoke_token(current_app.db, get_jwt())
    except Exception:
        pass

    try:
        logout_user()
    except Exception:
        pass

    return jsonify({"message": "Token révoqué. Supprimez le token côté client."}), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    identity = get_jwt_identity()
    users_col = current_app.db.users
    user_doc = users_col.find_one({"_id": ObjectId(identity)})

    if not user_doc:
        return jsonify({"error": "Utilisateur non trouvé"}), 404

    # 1. Génération du nouveau token ici
    new_access_token = create_access_token(identity=identity)

    # 2. Décodage du nouveau token pour obtenir sa date d'expiration
    decoded_token = decode_token(new_access_token)
    new_exp = decoded_token.get("exp")

    # 3. Sérialisation de l'utilisateur
    try:
        serialized = serialize_user(user_doc, include_local_localized=True)
    except Exception:
        serialized = None

    # 4. Formatage de la date d'expiration (Celle du nouveau token)
    token_exp_local = None
    try:
        from datetime import datetime, timezone

        token_exp_local = datetime.fromtimestamp(new_exp, timezone.utc).isoformat()
    except Exception:
        pass

    # 5. Création de la réponse JSON
    response = jsonify(
        {
            "user": serialized,
            "token_exp": new_exp,
            "token_exp_local": token_exp_local,
        }
    )

    # 6. On attache le token dans l'en-tête de réponse
    response.headers["X-Access-Token"] = new_access_token

    return response, 200


@auth_bp.route("/me", methods=["PATCH"])
@jwt_required()
def update_me():
    identity = get_jwt_identity()
    users_col = current_app.db.users
    data = request.get_json() or {}

    # Valider le payload
    is_valid, error_response = validate_user_update_profile(data)
    if not is_valid:
        return jsonify(error_response), 400

    # Champs que l'utilisateur peut mettre à jour lui-même
    allowed = {"first_name", "last_name", "password"}
    updates = {k: v for k, v in data.items() if k in allowed}
    password_changed = False
    if "password" in updates:
        from werkzeug.security import generate_password_hash

        updates["password"] = generate_password_hash(updates["password"])
        password_changed = True

    if not updates:
        return jsonify({"error": "Aucun champ modifiable fourni"}), 400

    updates["updated_at"] = datetime.utcnow()

    try:
        res = users_col.update_one({"_id": ObjectId(identity)}, {"$set": updates})
    except Exception as e:
        return jsonify({"error": "Erreur mise à jour", "detail": str(e)}), 500

    if res.matched_count == 0:
        return jsonify({"error": "Utilisateur non trouvé"}), 404

    user_doc = users_col.find_one({"_id": ObjectId(identity)})
    try:
        serialized = serialize_user(user_doc, include_local_localized=True)
    except Exception:
        serialized = None

    # Si le mot de passe a été modifié, révoquer le token courant
    if password_changed:
        from flask_jwt_extended import get_jwt
        from src.services.auth_utils import revoke_token

        revoke_token(current_app.db, get_jwt())
        return (
            jsonify(
                {
                    "message": "Mot de passe modifié, veuillez vous reconnecter.",
                    "user": serialized,
                }
            ),
            401,
        )
    return jsonify({"message": "Profil mis à jour", "user": serialized}), 200
