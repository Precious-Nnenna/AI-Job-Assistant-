from fastapi import APIRouter, Depends, HTTPException, status
from .auth_schema import UserCreate, UserOut, PasswordChange, ProfileUpdate
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .auth_models import User
from .password_hashing import hash_password, verify_password, DUMMY_HASH
from .token import create_access_token
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from .dependencies import get_current_user





router = APIRouter(prefix ="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user:UserCreate, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == user.email)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This email already exists" )

    hashed = hash_password(user.password)

    new_user = User( 
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=hashed,)
   
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user



@router.post("/login")
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):

    stmt = select(User).where(User.email == form_data.username)
    result = await db.execute(stmt)
    existing_user = result.scalar_one_or_none()

    # Prevent timing attack: always verify something
    hash_to_verify = existing_user.hashed_password if existing_user else DUMMY_HASH
    verified = verify_password(form_data.password, hash_to_verify)

    if not existing_user or not verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password" )

    #Once the email and password matches, create a token
    access_token = create_access_token(data={"sub": str(existing_user.id)}, expires_delta=timedelta(minutes=30)) 


    return {"access_token": access_token,"token_type": "bearer"}


    

@router.get("/", response_model=UserOut)
async def get_me(me: User = Depends(get_current_user)):
    return me


@router.post("/")
async def change_password(data: PasswordChange, current_user : User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):

    # 1. Check current password (use current_user, not User)
    verify = verify_password(data.current_password, current_user.hashed_password)

    if not verify:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect current password")   

    #hash password
    hashed = hash_password(data.new_password)

    #update the current password to the one

    current_user.hashed_password = hashed
    await db.commit()
    
    return {"message": "Password updated successfully"}

@router.patch("/", response_model=UserOut)
async def update_profile (data: ProfileUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):

    if data.first_name is not None:
        current_user.first_name = data.first_name

    if data.last_name is not None:
            current_user.last_name = data.last_name

    await db.commit()
    await db.refresh(current_user)

    return current_user

    




                