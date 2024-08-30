from sqlalchemy import and_
from app.core.database import SessionLocal
from app.models import label
from app.schema.label_schema import LabelCreate, LabelUpdate, LabelDelete


class LabelService(object):
    @staticmethod
    # 创建标签
    def label_create(labels: LabelCreate):
        db = SessionLocal()
        db_label = label.LabelTable(**labels.dict())
        db.add(db_label)
        db.commit()
        db.refresh(db_label)
        db.close()
        return db_label

    @staticmethod
    # 更新标签
    def update_label(labels: LabelUpdate):
        db = SessionLocal()
        db_label = db.query(label.LabelTable).filter(and_(label.LabelTable.is_delete == False,
                                                          label.LabelTable.label_name == labels.label_name)).first()
        if labels.new_name is not None:
            setattr(db_label, 'label_name', labels.new_name)
        if labels.new_description is not None:
            setattr(db_label, 'description', labels.new_description)
        setattr(db_label, 'updater', labels.updater)
        setattr(db_label, 'update_time', labels.update_time)
        db.commit()
        db.refresh(db_label)
        db.close()
        return db_label

    @staticmethod
    # 通过标签名获取标签
    def get_label(label_name: str):
        db = SessionLocal()
        db_label = db.query(label.LabelTable).filter(and_(label.LabelTable.is_delete == False,
                                                      label.LabelTable.label_name == label_name)).first()
        db.close()
        return db_label

    @staticmethod
    # 标签软删除
    def delete_label(labels: LabelDelete):
        db = SessionLocal()
        db_label = db.query(label.LabelTable).filter(and_(label.LabelTable.is_delete == False,
                                                          label.LabelTable.label_name == labels.label_name)).first()
        setattr(db_label, 'label_name', str(labels.delete_time).replace(':', '_'))
        setattr(db_label, 'is_delete', labels.is_delete)
        setattr(db_label, 'delete_time', labels.delete_time)
        setattr(db_label, 'delete_people', labels.delete_people)
        db.commit()
        db.refresh(db_label)

        # 对添加了该标签的文件删除该记录
        # files = FileLabelService.get_files(db, db_label.label_name)
        # for file in files:
        #     setattr(file, 'is_delete', True)
        #     db.commit()
        #     db.refresh(file)
        db.close()

        return db_label
