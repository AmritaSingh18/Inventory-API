from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schema import UserCreate, UserOut
from app.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(400, "Email already exists")
    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token({"sub": user.email, "id": user.id})
    return {"access_token": token, "token_type": "bearer"}
