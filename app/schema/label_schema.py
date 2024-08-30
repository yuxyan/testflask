import datetime

from pydantic import BaseModel


class LabelBase(BaseModel):
    label_name: str
    description: str
    is_delete: bool = False


class LabelCreate(LabelBase):
    creator: str
    creation_time: datetime.datetime


class LabelUpdate(LabelBase):
    updater: str
    update_time: datetime.datetime
    new_name: str | None = None
    new_description: str | None = None


class LabelDelete(LabelBase):
    delete_time: datetime.datetime
    is_delete: bool = True
    delete_people: str


class FileLabelBase(BaseModel):
    file_name: str
    label_name: str
    is_delete: bool = False


class FileLabelCreate(FileLabelBase):
    pass

