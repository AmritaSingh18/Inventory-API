from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def get_current_user(token: str = Depends(oauth2_scheme)):
    if not SECRET_KEY or not ALGORITHM:
        raise HTTPException(status_code=500, detail="Configuration error")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
