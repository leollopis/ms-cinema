from cryptography.fernet import Fernet
import os


import secrets


def generate_and_append_key():
    env_path = ".env"
    enc_key = Fernet.generate_key().decode()
    secret_key = secrets.token_urlsafe(64)

    # Read existing .env if present
    existing = ""
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            existing = f.read()

    # Check for existing keys
    already_enc = "ENCRYPTION_KEY=" in existing
    already_secret = "SECRET_KEY=" in existing

    with open(env_path, "a") as f:
        if not already_enc:
            f.write(f"\nENCRYPTION_KEY={enc_key}\n")
        else:
            print("ENCRYPTION_KEY already exists in .env")
        if not already_secret:
            f.write(f"SECRET_KEY={secret_key}\n")
        else:
            print("SECRET_KEY already exists in .env")

    print(f"Details: Generated and appended keys to {env_path}")
    if not already_enc:
        print(f"ENCRYPTION_KEY: {enc_key}")
    if not already_secret:
        print(f"SECRET_KEY: {secret_key}")


if __name__ == "__main__":
    generate_and_append_key()
