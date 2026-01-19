import os
import shutil
import secrets
from cryptography.fernet import Fernet

def ensure_env_and_keys():
    env_path = ".env"
    example_path = "exemple.env"

    # 1. Create .env from exemple.env if it doesn't exist
    if not os.path.exists(env_path):
        if os.path.exists(example_path):
            shutil.copy(example_path, env_path)
            print(f"Created {env_path} from {example_path}")
        else:
            # Fallback if no example file
            with open(env_path, "w") as f:
                f.write("# Generated .env\n")
            print(f"Created empty {env_path}")

    # 2. Read current .env
    with open(env_path, "r") as f:
        lines = f.readlines()

    env_map = {}
    for line in lines:
        if "=" in line and not line.strip().startswith("#"):
            key, val = line.strip().split("=", 1)
            env_map[key] = val

    has_enc = "ENCRYPTION_KEY" in env_map and env_map["ENCRYPTION_KEY"]
    has_sec = "SECRET_KEY" in env_map and env_map["SECRET_KEY"]

    # 3. Check conditions
    if has_enc and has_sec:
        print("Keys already present. Configuration OK.")
        return

    print("Keys missing or incomplete. Regenerating both...")

    # Generate new keys
    new_enc = Fernet.generate_key().decode()
    new_sec = secrets.token_urlsafe(64)

    # 4. Update file content
    # We will reconstruct the file to preserve comments/structure but replace keys
    new_lines = []
    keys_written = {"ENCRYPTION_KEY": False, "SECRET_KEY": False}

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("ENCRYPTION_KEY="):
            new_lines.append(f"ENCRYPTION_KEY={new_enc}\n")
            keys_written["ENCRYPTION_KEY"] = True
        elif stripped.startswith("SECRET_KEY="):
            new_lines.append(f"SECRET_KEY={new_sec}\n")
            keys_written["SECRET_KEY"] = True
        else:
            new_lines.append(line)
    
    # Append if not found existing line to replace
    if not keys_written["ENCRYPTION_KEY"]:
        if new_lines and not new_lines[-1].endswith("\n"):
            new_lines.append("\n")
        new_lines.append(f"ENCRYPTION_KEY={new_enc}\n")
    
    if not keys_written["SECRET_KEY"]:
         if new_lines and not new_lines[-1].endswith("\n"):
            new_lines.append("\n")
         new_lines.append(f"SECRET_KEY={new_sec}\n")

    with open(env_path, "w") as f:
        f.writelines(new_lines)

    print(f"Updated {env_path} with new keys.")

if __name__ == "__main__":
    ensure_env_and_keys()
