"""Nova AI — Firebase Admin SDK Integration"""

from __future__ import annotations

import json
import os
from typing import Any

from backend.core.config import settings
from backend.core.logging_config import NovaLogger

logger = NovaLogger("core.firebase")

_firebase_app: Any = None
_firebase_auth: Any = None


def _load_credentials() -> dict | None:
    """Load Firebase service account credentials."""
    path = settings.FIREBASE_CREDENTIALS_PATH
    if not os.path.exists(path):
        logger.warning("Firebase credentials file not found", path=path)
        return None
    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        logger.error("Failed to load Firebase credentials", error=str(e))
        return None


def init_firebase() -> bool:
    """Initialize Firebase Admin SDK. Returns True if successful."""
    global _firebase_app, _firebase_auth

    if _firebase_app is not None:
        return True

    if not settings.FIREBASE_PROJECT_ID:
        logger.info("Firebase not configured — using local auth fallback")
        return False

    try:
        import firebase_admin
        from firebase_admin import auth, credentials
    except ImportError:
        logger.warning("firebase-admin not installed — using local auth fallback")
        return False

    creds = _load_credentials()
    if creds is None:
        logger.warning("No Firebase credentials — using local auth fallback")
        return False

    try:
        cred = credentials.Certificate(creds)
        _firebase_app = firebase_admin.initialize_app(cred, {
            "projectId": settings.FIREBASE_PROJECT_ID,
        })
        _firebase_auth = auth
        logger.info("Firebase Admin initialized", project=settings.FIREBASE_PROJECT_ID)
        return True
    except Exception as e:
        logger.error("Firebase init failed", error=str(e))
        return False


def get_firebase_auth():
    """Get Firebase auth instance."""
    return _firebase_auth


def verify_firebase_token(id_token: str) -> dict | None:
    """Verify a Firebase ID token and return decoded claims."""
    auth = get_firebase_auth()
    if auth is None:
        return None
    try:
        decoded = auth.verify_id_token(id_token, check_revoked=True)
        return decoded
    except Exception as e:
        logger.warning("Firebase token verification failed", error=str(e))
        return None


def create_firebase_user(email: str, password: str, display_name: str = "") -> dict | None:
    """Create a Firebase Auth user."""
    auth = get_firebase_auth()
    if auth is None:
        return None
    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name or None,
        )
        logger.info("Firebase user created", uid=user.uid)
        return {"uid": user.uid, "email": user.email}
    except Exception as e:
        logger.error("Firebase user creation failed", error=str(e))
        raise


def send_password_reset(email: str) -> bool:
    """Send a password reset email via Firebase."""
    auth = get_firebase_auth()
    if auth is None:
        return False
    try:
        auth.generate_password_reset_link(email)
        logger.info("Password reset email sent", email=email)
        return True
    except Exception as e:
        logger.warning("Password reset failed", error=str(e))
        return False


def is_firebase_enabled() -> bool:
    return _firebase_app is not None
