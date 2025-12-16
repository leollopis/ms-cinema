from datetime import datetime
from os import getenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import psycopg

app = FastAPI(title="Auth Service", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"] ,
    allow_headers=["*"],
)


class RegisterPayload(BaseModel):
    email: EmailStr
    password: str


class LoginPayload(BaseModel):
    email: EmailStr
    password: str


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "service": "auth",
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "db": getenv("DB_NAME", "auth_db"),
    }


@app.get("/hello")
def hello_world_short() -> dict[str, str]:
    return {"status": "ok", "message": "Hello World"}


@app.get("/db-test")
def db_test() -> dict[str, str]:
    dsn = (
        f"host={getenv('DB_HOST', 'postgres')} "
        f"port={getenv('DB_PORT', '5432')} "
        f"dbname={getenv('DB_NAME', 'auth_db')} "
        f"user={getenv('DB_USER', 'auth_user')} "
        f"password={getenv('DB_PASSWORD', 'auth_pass')}"
    )

    try:
        with psycopg.connect(dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT current_database(), current_user")
                db_name, db_user = cur.fetchone()
        return {
            "status": "ok",
            "db": db_name,
            "user": db_user,
        }
    except Exception as exc:  # pragma: no cover - simple connectivity check
        raise HTTPException(status_code=500, detail={"status": "error", "message": str(exc)})


@app.post("/register")
def register(_: RegisterPayload) -> dict[str, str]:
    raise HTTPException(status_code=501, detail="Register endpoint not implemented yet")


@app.post("/login")
def login(_: LoginPayload) -> dict[str, str]:
    raise HTTPException(status_code=501, detail="Login endpoint not implemented yet")


@app.get("/me")
def me() -> dict[str, str]:
    raise HTTPException(status_code=501, detail="Me endpoint not implemented yet")
