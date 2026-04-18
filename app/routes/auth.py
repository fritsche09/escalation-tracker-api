from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from app.models.user import User
from app.schemas.user import UserRegister, UserLogin, UserResponse, Token
from app.database import get_db
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import timezone, datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = data.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not email:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return user

@router.post("/register", response_model=UserResponse, status_code=201)
def authorize(user: UserRegister, db: Session=Depends(get_db)):
    check_existing_email = db.query(User).filter(User.email == user.email).first()

    if check_existing_email:
        raise HTTPException(status_code=409, detail="Email already exists")
    
    hashed_password = pwd_context.hash(user.password)

    new_user = User(
        name = user.name,
        email = user.email,
        hashed_password = hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login", response_model=Token)
def login(user: OAuth2PasswordRequestForm=Depends(OAuth2PasswordRequestForm), db: Session=Depends(get_db)):
    get_user = db.query(User).filter(User.email == user.username).first()

    if not get_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    confirmed_password = pwd_context.verify(user.password, get_user.hashed_password)

    if not confirmed_password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    jwt_token = create_access_token({"sub": get_user.email})

    return Token(access_token=jwt_token) 
    


