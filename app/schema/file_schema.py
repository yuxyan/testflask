import datetime

from pydantic import BaseModel


class FileBase(BaseModel):
    file_name: str
    file_address: str
    file_type: str
    is_delete: bool = False
    download_number: int = 0


class FileCreate(FileBase):
    creator: str
    creation_time: datetime.datetime


class FileUpdate(FileBase):
    updater: str
    update_time: datetime.datetime


class FileDelete(FileBase):
    delete_time: datetime.datetime
    is_delete: bool = True
    delete_people: str

