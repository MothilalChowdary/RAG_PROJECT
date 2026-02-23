from database import SessionLocal, User
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def create_user(username, password, role):
    db = SessionLocal()
    hashed_pw = pwd_context.hash(password)
    user = User(username=username, password_hash=hashed_pw, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    print(f"User {username} added with ID {user.id}")
