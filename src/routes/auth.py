from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session


from src.services.auth import (create_access_token,
                               create_refresh_token,
                               get_email_form_refresh_token,
                               Hash)
from src.database.db import get_db
from src.database.models import User
from src.schemas import UserResponse, TokenModel, UserModel


app = APIRouter(prefix='/auth')

hash_handler = Hash()
security = HTTPBearer()


@app.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserModel, db: Session = Depends(get_db)):
    exist_user = db.query(User).filter(User.email == body.username).first()
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    body.password = hash_handler.get_password_hash(body.password)
    new_user = User(username=body.username, email=body.email, password=body.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"user": new_user, "detail": "User successfully created"}


@app.post("/login", response_model=TokenModel, status_code=status.HTTP_201_CREATED)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not hash_handler.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    # Generate JWT
    access_token = await create_access_token(data={"sub": user.email})
    refresh_token = await create_refresh_token(data={"sub": user.email})
    user.refresh_token = refresh_token
    db.commit()
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@app.get('/refresh_token', response_model=TokenModel)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    email = await get_email_form_refresh_token(token)
    user = db.query(User).filter(User.email == email).first()
    if user.refresh_token != token:
        user.refresh_token = None
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await create_access_token(data={"sub": email})
    refresh_token = await create_refresh_token(data={"sub": email})
    user.refresh_token = refresh_token
    db.commit()
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

