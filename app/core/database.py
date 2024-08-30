from functools import lru_cache

import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import Settings


@lru_cache
def get_settings():
    return Settings()


pymysql.install_as_MySQLdb()
# 配置化一些
SQLALCHEMY_DATABASE_URL = (f"mysql://{get_settings().MYSQL_USERNAME}:{get_settings().MYSQL_PASSWORD}@"
                           f"{get_settings().HOST}:{get_settings().PORT}/{get_settings().DB}")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
