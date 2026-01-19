from typing import Dict, Tuple, List

USER_SCHEMA_REGISTER = {
    "required": ["email", "password"],
    "optional": ["first_name", "last_name"],
}

USER_SCHEMA_LOGIN = {
    "required": ["email", "password"],
    "optional": [],
}

USER_SCHEMA_UPDATE_PROFILE = {
    "required": [],
    "optional": ["first_name", "last_name", "password"],
}


def validate_payload(payload: dict, schema: Dict[str, List[str]]) -> Tuple[bool, Dict]:
    """
    Valide un payload contre un schéma :
    1. Vérifie la présence des champs obligatoires.
    2. Vérifie l'absence de champs inconnus.
    3. SÉCURITÉ : Vérifie les types pour éviter l'injection NoSQL.
    """
    if not isinstance(payload, dict):
        return False, {"error": "Payload must be a dictionary"}

    # --- 1. Validation des clés (Requis / Inconnu) ---
    # (Garde ton code existant ici pour required/optional...)
    required = set(schema.get("required", []))
    optional = set(schema.get("optional", []))
    all_allowed = required | optional

    payload_keys = set(payload.keys())
    missing_required = required - payload_keys
    invalid_keys = payload_keys - all_allowed

    if missing_required or invalid_keys:
        error_response = {
            "error": "Validation échouée",
        }

        if missing_required:
            error_response["elements_obligatoires_manquants"] = sorted(
                list(missing_required)
            )

        if invalid_keys:
            error_response["elements_non_reconnus"] = sorted(list(invalid_keys))

        # Pour aider le développeur, on rappelle les champs optionnels autorisés
        error_response["elements_optionnels_acceptes"] = sorted(list(optional))

        return False, error_response

    # --- 2. SÉCURITÉ & TYPES : Définition des types attendus ---
    # Par défaut, tout est considéré comme du texte (str) pour la sécurité
    # On précise juste les exceptions (int, list, bool, etc.)
    field_types = {}

    type_errors = {}

    for key, value in payload.items():
        if value is None:
            continue

        # On récupère le type attendu (str par défaut)
        expected_type = field_types.get(key, str)

        if not isinstance(value, expected_type):
            type_name = expected_type.__name__
            type_errors[key] = (
                f"Type invalide. Attendu : {type_name}. Reçu : {type(value).__name__}"
            )

    if type_errors:
        return False, {
            "error": "Validation des types échouée (Sécurité)",
            "erreurs_type": type_errors,
        }

    return True, {}


def validate_user_register(payload: dict) -> Tuple[bool, Dict]:
    """Valide un payload pour l'enregistrement d'un nouvel utilisateur."""
    return validate_payload(payload, USER_SCHEMA_REGISTER)


def validate_user_login(payload: dict) -> Tuple[bool, Dict]:
    """Valide un payload pour la connexion d'un utilisateur."""
    return validate_payload(payload, USER_SCHEMA_LOGIN)


def validate_user_update_profile(payload: dict) -> Tuple[bool, Dict]:
    """Valide un payload pour la mise à jour du profil utilisateur."""
    return validate_payload(payload, USER_SCHEMA_UPDATE_PROFILE)
