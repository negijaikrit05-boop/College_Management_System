from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate
from auth import get_password_hash


# ✅ Create new user
def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ✅ Get user by email
def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


# ✅ Get all users
def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


# ✅ Delete user by email
def delete_user(db: Session, email: str) -> bool:
    user = db.query(User).filter(User.email == email).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False


# ✅ Update password
def update_user_password(db: Session, email: str, new_password: str) -> User | None:
    user = db.query(User).filter(User.email == email).first()
    if user:
        user.hashed_password = get_password_hash(new_password)
        db.commit()
        db.refresh(user)
        return user
    return None
