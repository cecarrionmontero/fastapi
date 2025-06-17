from auth.db import Base, engine, SessionLocal
from auth.models import User
from auth.jwt_handler import get_password_hash

# ⚠️ Ejecutar solo una vez para inicializar
def init_db():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    users = [
        User(username="admin", hashed_password=get_password_hash("VCg$yTB7W$2MY7E8L1Ww"), role="admin"),
        User(username="qubtis1", hashed_password=get_password_hash("sgA5quBPXG3L7Cq!jx6L"), role="user")
    ]
    for user in users:
        existing = db.query(User).filter_by(username=user.username).first()
        if not existing:
            db.add(user)
    db.commit()
    db.close()

if __name__ == "__main__":
    init_db()

