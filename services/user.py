from sqlalchemy.orm import Session
from models.user import CreateUser, UserResponse, UpdateUser
from database.models import UserTable
from auth.utils import hash_password


def create_user(db: Session, user: CreateUser) -> UserResponse:
    hashed = hash_password(user.password)
    new_user = UserTable(
        name=user.name,
        email=user.email,
        age=user.age,
        phone_number=user.phone_number,
        gender=user.gender,
        password=hashed,
        home_address=user.home_address,
        office_address=user.office_address,
        occupation=user.occupation,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_user(db: Session, user_id: int) -> UserResponse:
    return db.query(UserTable).filter(UserTable.id == user_id).first()


def update_user(db: Session, user_id: int, updated_user: CreateUser) -> UserResponse:
    user = db.query(UserTable).filter(UserTable.id == user_id).first()
    if user is None:
        return None
    user.name = updated_user.name
    user.email = updated_user.email
    user.age = updated_user.age
    user.phone_number = updated_user.phone_number
    user.gender = updated_user.gender
    user.home_address = updated_user.home_address
    user.office_address = updated_user.office_address
    user.occupation = updated_user.occupation
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(UserTable).filter(UserTable.id == user_id).first()
    if user is None:
        return False
    db.delete(user)
    db.commit()
    return True


def list_users(db: Session) -> list[UserResponse]:
    return db.query(UserTable).all()


def patch_user(db: Session, user_id: int, updated_fields: UpdateUser) -> UserResponse:
    user = db.query(UserTable).filter(UserTable.id == user_id).first()
    if user is None:
        return None
    patch_data = updated_fields.model_dump(exclude_none=True)
    for key, value in patch_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user
