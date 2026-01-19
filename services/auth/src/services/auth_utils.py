from datetime import datetime, timezone


def revoke_token(db, jwt_payload: dict) -> bool:
    try:
        jti = jwt_payload.get("jti")
        exp = jwt_payload.get("exp")
        if not jti or not exp:
            return False
        expires_at = datetime.fromtimestamp(exp, timezone.utc)
        db.jwt_blocklist.insert_one(
            {
                "jti": jti,
                "expires_at": expires_at,
                "created_at": datetime.now(timezone.utc),
            }
        )
        return True
    except Exception:
        return False
