
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt
from bson import ObjectId
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel, EmailStr, Field
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pwdlib import PasswordHash

# Load .env from the backend folder
BACKEND_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BACKEND_DIR / ".env")

router = APIRouter(prefix="/auth", tags=["Authentication"])

password_hash = PasswordHash.recommended()
bearer_scheme = HTTPBearer(auto_error=False)

MONGODB_URI = os.getenv("MONGODB_URI")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

if not MONGODB_URI:
    raise RuntimeError("MONGODB_URI is missing from the environment")

if not JWT_SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY is missing from the environment")

client = MongoClient(
    MONGODB_URI,
    serverSelectionTimeoutMS=10000
)
db = client["dermaai"]
users_collection = db["users"]

users_collection.create_index("email", unique=True)


# ========================================
# REQUEST MODELS
# ========================================

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


# ========================================
# REGISTRATION
# ========================================

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED
)
def register_doctor(data: RegisterRequest):
    name = data.name.strip()
    email = str(data.email).strip().lower()

    if len(name) < 2 or not re.search(r"[A-Za-z]", name):
        raise HTTPException(
            status_code=400,
            detail="Please enter a valid name."
        )

    user = {
        "name": name,
        "email": email,
        "password_hash": password_hash.hash(data.password),
        "role": "doctor",
        "created_at": datetime.now(timezone.utc),
    }

    try:
        result = users_collection.insert_one(user)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists."
        )

    return {
        "message": "Doctor account created successfully.",
        "user": {
            "id": str(result.inserted_id),
            "name": name,
            "email": email,
            "role": "doctor",
        },
    }


# ========================================
# LOGIN
# ========================================

@router.post("/login")
def login_doctor(data: LoginRequest):
    email = str(data.email).strip().lower()

    user = users_collection.find_one({"email": email})

    # Use the same error for unknown email and wrong password.
    if (
        not user
        or not password_hash.verify(
            data.password,
            user["password_hash"]
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    expires_at = datetime.now(timezone.utc) + timedelta(minutes=60)

    token_payload = {
        "sub": str(user["_id"]),
        "exp": expires_at,
    }

    access_token = jwt.encode(
        token_payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 3600,
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "role": user.get("role", "doctor"),
        },
    }


# ========================================
# CURRENT AUTHENTICATED DOCTOR
# ========================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    )
):
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please log in to access this resource.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(
            credentials.credentials,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM],
        )

        user_id = payload.get("sub")

        if not user_id or not ObjectId.is_valid(user_id):
            raise InvalidTokenError("Invalid user identifier")

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Your session is invalid or expired. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = users_collection.find_one(
        {"_id": ObjectId(user_id)}
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account not found.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "role": user.get("role", "doctor"),
    }


# ========================================
# VERIFY LOGIN SESSION
# ========================================

@router.get("/me")
def get_my_account(
    current_user: dict = Depends(get_current_user)
):
    return {"user": current_user}
