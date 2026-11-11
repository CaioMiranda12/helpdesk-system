"""Execute a partir de backend/: python -m scripts.create_admin"""
from getpass import getpass
from sqlalchemy import select
from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.user import User


def main():
    email = input("E-mail do administrador: ").strip().lower()
    name = input("Nome: ").strip()
    password = getpass("Senha (mínimo 12 caracteres): ")
    if not email or "@" not in email or len(name) < 2 or len(password) < 12:
        raise SystemExit("E-mail, nome ou senha inválidos.")
    with SessionLocal() as db:
        if db.scalar(select(User.id).where(User.email == email)) is not None:
            raise SystemExit("E-mail já cadastrado. Nenhum usuário foi criado.")
        db.add(User(email=email, name=name, password_hash=hash_password(password), role="admin"))
        db.commit()
    print("Administrador criado. Faça login em /api/v1/auth/login.")


if __name__ == "__main__":
    main()
