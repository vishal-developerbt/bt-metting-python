from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, auth
from app.database import get_db

router = APIRouter()

@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = auth.hash_password(user.password)

    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role= user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not auth.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = auth.create_access_token({
        "sub": str(db_user.id),
        "role": db_user.role,
        "email": db_user.email
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": db_user.role,
        "email": db_user.email
    }

# @router.post("/login")
# def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
#     db_user = db.query(models.User).filter(
#         models.User.email == user.email
#     ).first()

#     if not db_user or not auth.verify_password(user.password, db_user.password):
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     token = auth.create_access_token({
#         "sub": str(db_user.id),
#         "role": db_user.role,
#         "email": user.email
#     })

#     return {
#         "access_token": token,
#         "token_type": "bearer",
#         "role": db_user.role,  # optional but useful for frontend
#         "email": user.email
#     }



@router.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user