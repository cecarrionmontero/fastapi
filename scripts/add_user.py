from auth.db import SessionLocal
from auth.models import User
from auth.jwt_handler import get_password_hash

def add_user(username: str, password: str, role: str = "user"):
    db = SessionLocal()

    existing_user = db.query(User).filter_by(username=username).first()
    if existing_user:
        print(f"⚠️ Usuario '{username}' ya existe.")
        db.close()
        return

    new_user = User(
        username=username,
        hashed_password=get_password_hash(password),
        role=role
    )

    db.add(new_user)
    db.commit()
    db.close()
    print(f"✅ Usuario '{username}' creado con rol '{role}'.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Agregar usuario a la base de datos")
    parser.add_argument("username", help="Nombre de usuario")
    parser.add_argument("password", help="Contraseña")
    parser.add_argument("--role", default="user", help="Rol (por defecto: user)")

    args = parser.parse_args()

    add_user(args.username, args.password, args.role)

