from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.auth import LoginRequest, TokenResponse
# from services.user import user_db, user_passwords
from auth.utils import verify_password, create_access_token
from database.connection import get_db
from database.models import UserTable

router = APIRouter()

@router.post("/auth/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session=Depends(get_db)):
    user = db.query(UserTable).filter(UserTable.email==request.email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Wrong passwords")
    token=create_access_token({"sub":str(user.id)})
    return TokenResponse(access_token=token, token_type="bearer")
    
    #  for user in user_db:
    #     if user.email==request.email:
    #         if not verify_password(request.password, user_passwords[user.id]):
    #             raise HTTPException(status_code=401, detail="Wrong passwords")
    #         token=create_access_token({"sub":str(user.id)})
    #         return TokenResponse(access_token=token,token_type="bearer")
    # raise HTTPException(status_code=404, detail="User not found")    