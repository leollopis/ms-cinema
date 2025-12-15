from flask import Blueprint, jsonify, request, current_app
from src.models.user_model import User
from src.services.validation_service import validate_user_register

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    # 1. Validation (Assure-toi que validate_user_register ne vérifie plus le username !)
    is_valid, error_response = validate_user_register(data)
    if not is_valid:
        return jsonify(error_response), 400

    users_col = current_app.db.users

    # 2. Vérification d'unicité
    if User.get_by_email(users_col, data["email"]):
        return jsonify({"error": "Email déjà pris"}), 409

    # 3. Création de l'utilisateur
    # CORRECTION ICI : On n'appelle que les arguments définis dans ton modèle
    try:
        new_user = User.create(users_col, data["email"], data["password"])
        return jsonify({"message": "Compte créé", "id": new_user.id}), 201

    except Exception as e:
        # Capture d'une erreur inattendue pour le debug
        return jsonify({"error": str(e)}), 500
