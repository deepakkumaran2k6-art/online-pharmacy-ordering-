from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from app.core.database import SessionLocal
from app.core.security import create_access_token
from app.core.security import security, verify_access_token
from app.schemas.user import UserCreate
from app.services.user_service import create_user, verify_password
from app.models.user import User


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/signup")
def signup(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        user = create_user(db, user_data)

        return {
            "message": "User registered successfully",
            "user_id": user.user_id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/login")
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.email == login_data.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        login_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {
            "user_id": user.user_id,
            "email": user.email,
            "role": user.role
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me")
def get_current_user(
    credentials = Depends(security)
):
    payload = verify_access_token(credentials)

    return {
        "message": "Token is valid",
        "user_id": payload.get("user_id"),
        "email": payload.get("email"),
        "role": payload.get("role")
    }