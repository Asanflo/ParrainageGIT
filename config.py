import os
from datetime import timedelta
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

class Config:
    # =========================
    # Flask
    # =========================
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    DEBUG = os.getenv("FLASK_DEBUG", "True") == "True"

    # =========================
    # Base de données PostgreSQL
    # =========================
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")  # <-- Render injecte ça automatiquement
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # =========================
    # JWT
    # =========================
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.getenv("JWT_ACCESS_EXPIRES_HOURS", 6))
    )

    # =========================
    # Sécurité & API
    # =========================
    JSON_SORT_KEYS = False

    # =========================
    # Sécurité système
    # =========================
    SYSTEM_ASSIGN_KEY = os.getenv("SYSTEM_ASSIGN_KEY")

    # =========================
    # CORS
    # =========================
    # URL(s) autorisée(s) pour le frontend
    # Exemple: FRONTEND_URL=https://mon-frontend.vercel.app
    CORS_ORIGINS = os.getenv("FRONTEND_URL", "*")  # "*" pour autoriser toutes les origines (dev uniquement)