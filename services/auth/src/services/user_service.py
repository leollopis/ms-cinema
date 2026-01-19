from datetime import datetime, timezone
from bson.objectid import ObjectId


def serialize_user(user_doc: dict, include_local_localized: bool = True) -> dict:
    if not user_doc:
        return None

    user = dict(user_doc)

    # 1. On retire le mot de passe hashé
    user.pop("password", None)

    # 2. On convertit l'ID principal
    user["id"] = str(user.get("_id"))
    user.pop("_id", None)

    # 3. Gestion des dates
    for fld in ("created_at", "updated_at", "last_login_at"):
        dt = user.get(fld)
        if isinstance(dt, datetime):
            user[fld] = dt.isoformat()
        else:
            user[fld] = None

    return user


def update_last_login(users_col, user_id: str) -> None:
    try:
        users_col.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"last_login_at": datetime.now(timezone.utc)}},
        )
    except Exception:
        pass
