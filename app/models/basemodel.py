from sqlalchemy import Column, String, Boolean, DATETIME


class BaseModel:
    creator = Column(String(50))
    creation_time = Column(DATETIME)
    updater = Column(String(50))
    update_time = Column(DATETIME)
    delete_time = Column(DATETIME)
    is_delete = Column(Boolean, default=0)
    delete_people = Column(String(50))
