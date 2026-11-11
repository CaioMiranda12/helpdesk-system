from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import UserRead

router = APIRouter(prefix="/api/v1/agents", tags=["Agentes"], dependencies=[Depends(get_current_user)])


@router.get("", response_model=list[UserRead])
def list_agents(db: Session = Depends(get_db)):
    return list(db.scalars(select(User).where(User.role == "agent").order_by(User.name, User.id)).all())
