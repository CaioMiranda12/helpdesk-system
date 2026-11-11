from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.security import create_access_token, get_current_user, hash_password, require_admin, verify_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse, UserCreate, UserRead

router = APIRouter(prefix="/api/v1", tags=["Autenticação"])


@router.post("/auth/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == str(payload.email).lower()))
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos")
    return TokenResponse(access_token=create_access_token(user), user=UserRead.model_validate(user))


@router.get("/auth/me", response_model=UserRead)
def me(user: User = Depends(get_current_user)):
    return user


@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db), _admin: User = Depends(require_admin)):
    email = str(payload.email).lower()
    if db.scalar(select(User.id).where(User.email == email)) is not None:
        raise HTTPException(status_code=409, detail="E-mail já cadastrado")
    user = User(email=email, name=payload.name, password_hash=hash_password(payload.password), role=payload.role.value)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/users", response_model=list[UserRead])
def list_users(
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    from fastapi import Query
    # Validamos explicitamente para manter a paginação previsível.
    if not 1 <= limit <= 100 or offset < 0:
        raise HTTPException(status_code=422, detail="Paginação inválida")
    return db.scalars(select(User).order_by(User.created_at.desc(), User.id).limit(limit).offset(offset)).all()
