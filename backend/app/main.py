
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.analyze import router as analyze_router
from app.auth import router as auth_router
from app.api.history import router as history_router

# ========================================
# FASTAPI APPLICATION
# ========================================

app = FastAPI(
    title="AI Skin Lesion Analysis API",
    description=(
        "AI-assisted skin lesion analysis "
        "system for doctors"
    ),
    version="1.0.0"
)


# ========================================
# CORS
# ========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        *[
            origin.strip()
            for origin in os.getenv("CORS_ORIGINS", "").split(",")
            if origin.strip()
        ],
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========================================
# ANALYSIS ROUTER
# ========================================

app.include_router(
    analyze_router
)


# ========================================
# AUTHENTICATION ROUTER
# ========================================

app.include_router(
    auth_router
)

app.include_router(history_router)
# ========================================
# ROOT
# ========================================

@app.get("/")
def root():
    return {
        "message": (
            "AI Skin Lesion Analysis API "
            "is running"
        )
    }
