"""Nova AI — Auth API Router

Handles registration, login (local + Firebase), token refresh,
password reset, profile retrieval, and logout.
"""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.config import settings
from backend.core.dependencies import get_current_user
from backend.core.firebase import (
    create_firebase_user,
    init_firebase,
    is_firebase_enabled,
    send_password_reset,
    verify_firebase_token,
)
from backend.core.logging_config import NovaLogger
from backend.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from backend.database.models import User, UserSettings
from backend.database.session import get_session
from backend.models.schemas import (
    AuthStatusResponse,
    FirebaseLoginRequest,
    PasswordResetRequest,
    RefreshTokenRequest,
    SuccessResponse,
    TokenResponse,
    UserLoginRequest,
    UserProfile,
    UserRegisterRequest,
)

logger = NovaLogger("api.auth")
router = APIRouter()

# Initialize Firebase on module load
init_firebase()


def _user_to_profile(user: User) -> UserProfile:
    return UserProfile(
        id=user.id,
        name=user.name,
        email=user.email,
        avatar_url=user.avatar_url,
        language=user.language,
        voice_id=user.voice_id,
        plan=user.plan,
        created_at=user.created_at,
        last_active=user.last_active,
    )


async def _create_user_in_db(
    session: AsyncSession,
    name: str,
    email: str,
    password_hash: str,
    firebase_uid: str | None = None,
) -> User:
    """Create a user record in the local database. Also creates default settings."""
    existing = await session.execute(select(User).where(User.email == email))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user = User(
        name=name,
        email=email,
        password_hash=password_hash,
        firebase_uid=firebase_uid,
    )
    session.add(user)
    await session.flush()

    settings = UserSettings(user_id=user.id)
    session.add(settings)
    await session.flush()

    return user


def _generate_tokens(user_id: str) -> dict:
    """Create access + refresh token pair."""
    access = create_access_token(subject=user_id)
    refresh = create_refresh_token(subject=user_id)
    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }


# ── Register ──────────────────────────────────────────────────────────────────

@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(body: UserRegisterRequest, session: AsyncSession = Depends(get_session)):
    """Register a new user. Uses Firebase if available, otherwise local auth."""
    pwd_hash = hash_password(body.password)
    firebase_uid = None

    if is_firebase_enabled():
        try:
            fb_user = create_firebase_user(
                email=body.email,
                password=body.password,
                display_name=body.name,
            )
            if fb_user:
                firebase_uid = fb_user["uid"]
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Firebase registration failed: {e}",
            )

    user = await _create_user_in_db(session, body.name, body.email, pwd_hash, firebase_uid)
    await session.commit()
    tokens = _generate_tokens(user.id)
    logger.info("User registered", user_id=user.id, email=user.email)
    return tokens


# ── Login (local) ─────────────────────────────────────────────────────────────

@router.post("/login", response_model=TokenResponse)
async def login(body: UserLoginRequest, session: AsyncSession = Depends(get_session)):
    """Authenticate with email + password (local bcrypt)."""
    result = await session.execute(select(User).where(User.email == body.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account deactivated",
        )

    user.last_active = datetime.now(timezone.utc)
    await session.commit()

    tokens = _generate_tokens(user.id)
    logger.info("User logged in", user_id=user.id)
    return tokens


# ── Firebase Login ────────────────────────────────────────────────────────────

@router.post("/firebase", response_model=TokenResponse)
async def login_firebase(body: FirebaseLoginRequest, session: AsyncSession = Depends(get_session)):
    """Authenticate with a Firebase ID token (Google or email sign-in)."""
    if not is_firebase_enabled():
        raise HTTPException(status_code=503, detail="Firebase is not configured")

    decoded = verify_firebase_token(body.id_token)
    if not decoded:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Firebase token",
        )

    fb_uid = decoded.get("uid")
    fb_email = decoded.get("email", "")
    fb_name = decoded.get("name") or body.name or ""
    fb_picture = decoded.get("picture") or body.avatar_url

    result = await session.execute(select(User).where(User.firebase_uid == fb_uid))
    user = result.scalar_one_or_none()

    if not user:
        result = await session.execute(select(User).where(User.email == fb_email))
        user = result.scalar_one_or_none()
        if user:
            user.firebase_uid = fb_uid
        else:
            user = await _create_user_in_db(
                session,
                name=fb_name,
                email=fb_email,
                password_hash="",
                firebase_uid=fb_uid,
            )
            if fb_picture:
                user.avatar_url = fb_picture

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account deactivated")

    user.last_active = datetime.now(timezone.utc)
    await session.commit()

    tokens = _generate_tokens(user.id)
    return tokens


# ── Token Refresh ─────────────────────────────────────────────────────────────

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(body: RefreshTokenRequest):
    """Exchange a refresh token for a new access token."""
    try:
        payload = decode_token(body.refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
            )
        tokens = _generate_tokens(user_id)
        return tokens
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )


# ── Password Reset ────────────────────────────────────────────────────────────

@router.post("/password-reset", response_model=SuccessResponse)
async def password_reset(body: PasswordResetRequest):
    """Send a password reset email via Firebase."""
    if is_firebase_enabled():
        success = send_password_reset(body.email)
    else:
        success = False

    if not success:
        logger.info("Password reset requested (firebase not available)", email=body.email)

    return SuccessResponse(
        message="Password reset email sent if the account exists",
    )


# ── Logout ────────────────────────────────────────────────────────────────────

@router.post("/logout", response_model=SuccessResponse)
async def logout(user: User = Depends(get_current_user)):
    """Logout (client-side token discard; server-side is a no-op with stateless JWTs)."""
    logger.info("User logged out", user_id=user.id)
    return SuccessResponse(message="Logged out successfully")


# ── Profile / Me ──────────────────────────────────────────────────────────────

@router.get("/me", response_model=UserProfile)
async def get_me(user: User = Depends(get_current_user)):
    """Get the authenticated user's profile."""
    return _user_to_profile(user)


@router.get("/status", response_model=AuthStatusResponse)
async def auth_status(user: User | None = Depends(get_current_user)):
    """Check authentication status."""
    if user is None:
        return AuthStatusResponse(authenticated=False, user=None)
    return AuthStatusResponse(authenticated=True, user=_user_to_profile(user))
