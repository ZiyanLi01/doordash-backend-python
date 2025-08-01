from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from pydantic import BaseModel
import uvicorn

from database import get_db, engine
from models import Base, User, Restaurant, MenuItem
from schemas import (
    UserCreate, UserLogin, UserResponse, 
    RestaurantCreate, RestaurantResponse,
    MenuItemCreate, MenuItemResponse,
    Token, TokenData
)

# Create database tables (with error handling for deployment)
try:
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")
except Exception as e:
    print(f"⚠️  Warning: Could not create database tables on startup: {e}")
    print("   This is normal during deployment if database is not yet available")

app = FastAPI(
    title="Mini DoorDash Backend",
    description="FastAPI backend for Mini DoorDash application",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Utility functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Health check endpoint
@app.get("/health")
async def health_check():
    # Check database connection
    db_status = "UNKNOWN"
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        db_status = "UP"
    except Exception as e:
        db_status = f"DOWN: {str(e)[:100]}"
    
    return {
        "status": "UP",
        "service": "Mini DoorDash Backend",
        "database": db_status,
        "timestamp": datetime.now().timestamp(),
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

@app.get("/")
async def root():
    return {
        "status": "UP",
        "message": "Mini DoorDash Backend is running",
        "timestamp": datetime.now().timestamp()
    }

# User endpoints
@app.post("/users/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        full_name=db_user.full_name,
        is_active=db_user.is_active
    )

@app.post("/users/login", response_model=Token)
async def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_credentials.username).first()
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/check-username/{username}")
async def check_username(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    return {"available": user is None}

@app.get("/users/check-email/{email}")
async def check_email(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    return {"available": user is None}

@app.get("/users/me", response_model=UserResponse)
async def get_current_user(username: str = Depends(verify_token), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active
    )

# Restaurant endpoints
@app.post("/restaurants", response_model=RestaurantResponse)
async def create_restaurant(
    restaurant: RestaurantCreate, 
    db: Session = Depends(get_db),
    username: str = Depends(verify_token)
):
    db_restaurant = Restaurant(**restaurant.dict())
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return RestaurantResponse(**db_restaurant.__dict__)

@app.get("/restaurants", response_model=List[RestaurantResponse])
async def get_restaurants(db: Session = Depends(get_db)):
    restaurants = db.query(Restaurant).all()
    return [RestaurantResponse(**restaurant.__dict__) for restaurant in restaurants]

@app.get("/restaurants/{restaurant_id}", response_model=RestaurantResponse)
async def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return RestaurantResponse(**restaurant.__dict__)

# Menu item endpoints
@app.post("/menu-items", response_model=MenuItemResponse)
async def create_menu_item(
    menu_item: MenuItemCreate, 
    db: Session = Depends(get_db),
    username: str = Depends(verify_token)
):
    db_menu_item = MenuItem(**menu_item.dict())
    db.add(db_menu_item)
    db.commit()
    db.refresh(db_menu_item)
    return MenuItemResponse(**db_menu_item.__dict__)

@app.get("/menu-items", response_model=List[MenuItemResponse])
async def get_menu_items(restaurant_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(MenuItem)
    if restaurant_id:
        query = query.filter(MenuItem.restaurant_id == restaurant_id)
    menu_items = query.all()
    return [MenuItemResponse(**item.__dict__) for item in menu_items]

@app.get("/menu-items/{menu_item_id}", response_model=MenuItemResponse)
async def get_menu_item(menu_item_id: int, db: Session = Depends(get_db)):
    menu_item = db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()
    if not menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return MenuItemResponse(**menu_item.__dict__)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
