from app.core.database import Base
from sqlalchemy import Column, String, ForeignKey, Boolean


class FileLabelTable(Base):
    __tablename__ = 'FileLabelTable'
    file_name = Column(String(50), ForeignKey("FileTable.file_name", onupdate='CASCADE', ondelete='CASCADE'),
                       primary_key=True)
    label_name = Column(String(50), ForeignKey("LabelTable.label_name", onupdate='CASCADE', ondelete='CASCADE'),
                        primary_key=True)
    is_delete = Column(Boolean)
