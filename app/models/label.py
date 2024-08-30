from sqlalchemy.orm import relationship
from sqlalchemy import Column, String

from app.core.database import Base
from app.models.basemodel import BaseModel
from app.models.filelabeltable import FileLabelTable


class LabelTable(Base, BaseModel):
    __tablename__ = 'LabelTable'
    label_name = Column(String(50), primary_key=True)
    description = Column(String(200))

    files = relationship("FileLabelTable")
