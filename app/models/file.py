from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer

from app.core.database import Base
from app.models.basemodel import BaseModel
from app.models.filelabeltable import FileLabelTable


class FileTable(Base, BaseModel):
    __tablename__ = 'FileTable'
    file_name = Column(String(50), primary_key=True)
    file_address = Column(String(200))
    file_type = Column(String(100))
    download_number = Column(Integer)

    labels = relationship("FileLabelTable")
