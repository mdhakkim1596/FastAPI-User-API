from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.user import CreateUser, UserResponse, UpdateUser
from services.user import (
    create_user,
    get_user,
    update_user,
    delete_user,
    list_users,
    patch_user,
)
from auth.utils import get_current_user
from database.connection import get_db

router = APIRouter()


@router.get("/users", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db), current_user: int = Depends(get_current_user)
):
    return list_users(db)


@router.post("/users", response_model=UserResponse)
def create_new_users(user: CreateUser, db: Session = Depends(get_db)):
    return create_user(db, user)


@router.get("/users/{id}", response_model=UserResponse)
def get_single_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    user = get_user(db, id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{id}", response_model=UserResponse)
def update_existing_user(
    id: int,
    user: CreateUser,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    updated = update_user(db, id, user)
    if updated is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.delete("/users/{id}")
def remove_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    deleted = delete_user(db, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}


@router.patch("/users/{id}", response_model=UserResponse)
def patch_existing_user(
    id: int,
    user: UpdateUser,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    patched = patch_user(db, id, user)
    if patched is None:
        raise HTTPException(status_code=404, detail="User not found")
    return patched
