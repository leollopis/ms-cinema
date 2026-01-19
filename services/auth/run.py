from generate_key import ensure_env_and_keys

# Ensure .env and keys exist before verifying/loading config
ensure_env_and_keys()

from src import create_app

app = create_app()

if __name__ == "__main__":
    # Debug=True permet le rechargement auto quand on modifie le code
    app.run(host="0.0.0.0", port=5000, debug=True)
