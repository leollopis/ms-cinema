from datetime import datetime, timezone
from os import getenv
from flask import Blueprint, jsonify, current_app

misc_bp = Blueprint("misc", __name__)

@misc_bp.route("/health", methods=["GET"])
def health():
    return jsonify({
        "service": "auth",
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "db": getenv("MONGO_DB", "authdb"),
    })

@misc_bp.route("/hello", methods=["GET"])
def hello_world_short():
    return jsonify({"status": "ok", "message": "Hello World"})

@misc_bp.route("/db-test", methods=["GET"])
def db_test():
    try:
        # Check Mongo connection
        current_app.db.command("ping")
        return jsonify({
            "status": "ok",
            "db": current_app.config["MONGO_DB"],
            "user": current_app.config["MONGO_USER"],
            "type": "mongodb"
        })
    except Exception as exc:
        return jsonify({"status": "error", "message": str(exc)}), 500
