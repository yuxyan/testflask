import datetime
import os

from flask import send_from_directory
from sqlalchemy import and_

from app.schema.file_schema import FileCreate, FileUpdate, FileDelete
from app.core.database import SessionLocal
from app.models import file


def rename_file(file_address: str, new_name: str, file_type: str):
    new_address = ""
    for i in file_address.split('/')[0:-1]:
        new_address = new_address + i + '/'
    new_address = new_address + new_name + '.' + file_type
    os.rename(file_address, new_address)


class FileService(object):
    @staticmethod
    def secure_filename(filename):

        if filename[0] == "/":
            filename = filename[1:]

        filename = filename.replace('/', '')
        filename = filename.replace('.', '')

        return filename

    @staticmethod
    def get_file(file_name: str):
        db = SessionLocal()
        db_file = db.query(file.FileTable).filter(and_(file.FileTable.is_delete == False,
                                                       file.FileTable.file_name == file_name)).first()
        db.close()
        return db_file

    @staticmethod
    def file_create(files: FileCreate):
        db = SessionLocal()
        db_file = file.FileTable(**files.dict())
        db.add(db_file)
        db.commit()
        db.refresh(db_file)
        db.close()
        return db_file

    @staticmethod
    def file_update(files: FileUpdate):
        db = SessionLocal()
        db_file = db.query(file.FileTable).filter(and_(file.FileTable.is_delete == False,
                                                       file.FileTable.file_name == files.file_name)).first()
        setattr(db_file, 'updater', files.updater)
        setattr(db_file, 'update_time', files.update_time)
        db.commit()
        db.refresh(db_file)
        db.close()
        return db_file

    @staticmethod
    def rename_db_file(old_name: str, new_name: str, update_time: datetime.datetime, updater: str):
        db = SessionLocal()
        db_file = db.query(file.FileTable).filter(and_(file.FileTable.is_delete == False,
                                                       file.FileTable.file_name == old_name)).first()
        new_address = ""
        for i in db_file.file_address.split('/')[0:-1]:
            new_address = new_address + i + '/'
        new_address = new_address + new_name + '.' + db_file.file_type
        os.rename(db_file.file_address, new_address)
        setattr(db_file, 'file_name', new_name)
        setattr(db_file, 'file_address', new_address)
        setattr(db_file, 'update_time', update_time)
        setattr(db_file, 'updater', updater)
        db.commit()
        db.refresh(db_file)
        db.close()
        return db_file

    @staticmethod
    def delete_file(files: FileDelete):
        db = SessionLocal()
        db_file = db.query(file.FileTable).filter(and_(file.FileTable.is_delete == False,
                                                       file.FileTable.file_name == files.file_name)).first()
        setattr(db_file, 'file_name', str(files.delete_time).replace(':', '_'))
        setattr(db_file, 'is_delete', files.is_delete)
        setattr(db_file, 'delete_time', files.delete_time)
        setattr(db_file, 'delete_people', files.delete_people)
        db.commit()
        db.refresh(db_file)

        # 删除该文件的标签记录
        # labels = FileLabelService.get_labels(db, db_file.file_name)
        # for label in labels:
        #     setattr(label, 'is_delete', True)
        #     db.commit()
        #     db.refresh(label)

        rename_file(db_file.file_address, db_file.file_name, db_file.file_type)
        return db_file

    @staticmethod
    def download(file_name: str):
        db = SessionLocal()
        db_file = (db.query(file.FileTable)
                   .filter(and_(file.FileTable.is_delete == False,
                                file.FileTable.file_name == ''.join(file_name.split(".")[0:-1]))).first())
        setattr(db_file, 'download_number', db_file.download_number + 1)
        db.commit()
        db.refresh(db_file)
        db.close()
        return send_from_directory("static/uploadfile", file_name, as_attachment=True)
