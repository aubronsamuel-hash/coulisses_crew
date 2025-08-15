from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import bcrypt
import secrets
import os

from . import storage

router = APIRouter()
security = HTTPBearer()
tokens: dict[str, int] = {}


class UserIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    role: str


class TokenRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str


class NotificationPrefsIn(BaseModel):
    email: str | None = None
    telegram: str | None = None
    telegram_chat_id: int | None = None


class NotificationPrefs(NotificationPrefsIn):
    pass


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user_id = tokens.get(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    data = storage.load_data()
    user = next((u for u in data["users"] if u["id"] == user_id), None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    return user


def require_role(role: str):
    def dependency(user: dict = Depends(get_current_user)):
        if user["role"] != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden"
            )
        return user

    return dependency


@router.post("/register", response_model=UserOut)
def register(user: UserIn):
    data = storage.load_data()
    if any(u["username"] == user.username for u in data["users"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
        )
    hashed = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
    user_id = len(data["users"]) + 1
    new_user = {
        "id": user_id,
        "username": user.username,
        "password_hash": hashed,
        "role": "intermittent",
    }
    data["users"].append(new_user)
    storage.save_data(data)
    return {"id": user_id, "username": user.username, "role": "intermittent"}


@router.post("/token-json", response_model=TokenResponse)
def token_json(req: TokenRequest):
    data = storage.load_data()
    user = next((u for u in data["users"] if u["username"] == req.username), None)
    if not user or not bcrypt.checkpw(
        req.password.encode(), user["password_hash"].encode()
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    token = secrets.token_hex(16)
    tokens[token] = user["id"]
    return {"access_token": token}


@router.get("/me", response_model=UserOut)
def me(user: dict = Depends(get_current_user)):
    return {"id": user["id"], "username": user["username"], "role": user["role"]}


@router.put("/me/prefs", response_model=NotificationPrefs)
def update_prefs(prefs: NotificationPrefsIn, user: dict = Depends(get_current_user)):
    data = storage.load_data()
    user_rec = next(u for u in data["users"] if u["id"] == user["id"])
    current = user_rec.get("notification_prefs", {})
    new_vals = prefs.model_dump(exclude_unset=True)
    current.update(new_vals)
    user_rec["notification_prefs"] = current
    storage.save_data(data)
    return current


@router.post("/me/notify-test")
def notify_test(user: dict = Depends(get_current_user)):
    data = storage.load_data()
    user_rec = next(u for u in data["users"] if u["id"] == user["id"])
    prefs = user_rec.get("notification_prefs", {})
    dry = os.getenv("NOTIFY_DRY_RUN", "0") == "1"
    print(f"notify-test: user {user['id']} prefs={prefs} dry_run={dry}")
    return {"ok": True, "dry_run": dry}
