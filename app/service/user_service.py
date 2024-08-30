import hashlib

from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models import user
from app.schema import user_schema


# 密码Hash
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


class UserService(object):
    @staticmethod
    # 获取用户
    def get_user(username: str):
        db = SessionLocal()
        db_user = db.query(user.User).filter(user.User.username == username).first()
        db.close()
        return db_user

    @staticmethod
    # 密码Hash
    def hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    @staticmethod
    def user_login(username: str, password: str):
        db = SessionLocal()
        db_user = db.query(user.User).filter(and_(user.User.username == username,
                                                  user.User.password == password)).first()
        db.close()
        return db_user

    @staticmethod
    def user_register(users: user_schema.UserCreate):
        db = SessionLocal()
        db_user = user.User(**users.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        db.close()
        return db_user
