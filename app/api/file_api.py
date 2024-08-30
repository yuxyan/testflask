import os
import time
from datetime import datetime

from flask import Blueprint, request, render_template, abort
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models.file_form import UploadForm, RenameForm, DeleteForm
from app.service.file_service import FileService
from app.schema.file_schema import FileCreate, FileUpdate, FileDelete
from app.core.redis import redis_client

from  app.celery_task.tasks import savefile2redis, test_task

file_api = Blueprint('file_api', __name__)
FILEPATH = "static/uploadfile/"


class FileApi:
    @staticmethod
    @file_api.route('/upload', methods=['POST', 'GET'])
    # @jwt_required()
    def upload_file():
        form = UploadForm()
        # username = get_jwt_identity()
        username = "ROOT"
        if request.method == 'GET':
            return render_template('upload_file.html', form=form)
        if form.validate_on_submit():
            file = form.file.data
            filename = file.filename
            file_type = ''.join(filename.split(".")[-1])
            filename = ''.join(filename.split(".")[0:-1])
            filename = FileService.secure_filename(filename)
            upload_time = datetime.now()
            # print(filename)
            if FileService.get_file(filename) is not None:
                abort(400)

            path = filename+'.'+file_type
            # 文件保存路径
            file_path = os.path.join(FILEPATH, path)
            # print(file_path)

            # 数据库添加记录
            file_create = FileCreate(file_name=filename, file_address=file_path,
                                     file_type=file_type, is_delete=False,
                                     download_number=0, creator=username, creation_time=upload_time)
            db_file = FileService.file_create(file_create)

            # 保存文件
            file.save(file_path)

            # 缓存？？
            start_time = time.time()
            with open(file_path, 'rb') as files:
                s = files.read()
            # print(time.time() - start_time)
            start_time = time.time()
            # --异步 filename s deadline
            # redis_client.set(filename, s)
            # redis_client.expire(filename, 3600)
            savefile2redis.apply_async(args=[filename, s])
            # print(time.time() - start_time)

            data = {
                "filename": filename,
                "upload_time": upload_time
            }
            return {
                "code": 0,
                "msg": "成功",
                "data": data,
            }

    @staticmethod
    @file_api.route('/update_file', methods=['POST', 'GET'])
    @jwt_required()
    def update():
        form = UploadForm()
        username = get_jwt_identity()

        if request.method == 'GET':
            return render_template('upload_file.html', form=form)
        if form.validate_on_submit():
            file = form.file.data
            filename = file.filename
            update_time = datetime.now()
            db_file = FileService.get_file(''.join(filename.split(".")[0:-1]))
            if db_file is None:
                abort(400)
            file_path = db_file.file_address
            file_update = FileUpdate(file_name=''.join(file.filename.split(".")[0:-1]), file_address=file_path,
                                     file_type=''.join(file.filename.split(".")[-1]), is_delete=False,
                                     download_number=0, updater=username, update_time=update_time)
            FileService.file_update(file_update)
            file.save(file_path)

            data = {
                "filename": filename,
                "updater": username,
                "upload_time": update_time
            }
            return {
                "code": 0,
                "msg": "成功",
                "data": data,
            }

    @staticmethod
    @file_api.route('/rename_file', methods=['POST', 'GET'])
    @jwt_required()
    def rename_file():
        form = RenameForm()
        username = get_jwt_identity()
        if request.method == 'GET':
            return render_template('rename_file.html', form=form)
        if form.validate_on_submit():
            update_time = datetime.now()
            old_name = form.old_name.data
            new_name = form.new_name.data
            new_name = FileService.secure_filename(new_name)
            db_file = FileService.get_file(old_name)
            if db_file is None:
                abort(400)
            db_new_file = FileService.get_file(new_name)
            if db_new_file is not None:
                abort(400)
            FileService.rename_db_file(old_name, new_name, update_time, username)
            data = {
                "filename": new_name,
                "updater": username,
                "upload_time": update_time
            }
            return {
                "code": 0,
                "msg": "成功",
                "data": data,
            }

    @staticmethod
    @file_api.route('/delete_file', methods=['POST', 'GET'])
    @jwt_required()
    def delete():
        form = DeleteForm()
        username = get_jwt_identity()
        if request.method == 'GET':
            return render_template('delete_file.html', form=form)
        if form.validate_on_submit():
            delete_time = datetime.now()
            file_name = form.file_name.data
            db_file = FileService.get_file(file_name)
            if db_file is None:
                abort(400)
            file_delete = FileDelete(file_name=db_file.file_name, file_address=db_file.file_address,
                                     file_type=db_file.file_type, is_delete=True, delete_time=delete_time,
                                     delete_people=username)
            FileService.delete_file(file_delete)
            data = {
                "delete_people": username,
                "delete_time": delete_time
            }
            return {
                "code": 0,
                "msg": "成功",
                "data": data,
            }

    # 文件下载
    @staticmethod
    @file_api.route('/download/<file_name>', methods=['POST', 'GET'])
    def download(file_name):
        db_file = FileService.get_file(''.join(file_name.split(".")[0:-1]))
        if db_file is None:
            abort(404)
        return FileService.download(file_name)

    # 在线查看文件内容
    @staticmethod
    @file_api.route('/show/<file_name>', methods=['POST', 'GET'])
    def show(file_name):
        start_time = time.time()
        file = redis_client.get(''.join(file_name.split(".")[0:-1]))
        print(time.time() - start_time)
        if file is not None:
            data = str(file)
        else:
            db_file = FileService.get_file(''.join(file_name.split(".")[0:-1]))
            if db_file is None:
                abort(404)
            start_time = time.time()
            with open(db_file.file_address, 'rb') as f:
                s = f.read()
            print(time.time() - start_time)
            redis_client.set(db_file.file_name, s)
            redis_client.expire(db_file.file_name, 3600)
            data = str(s)
        return {
            "code": 0,
            "msg": "成功",
            "data": data
        }

    @staticmethod
    @file_api.route("/test", methods=['POST', 'GET'])
    def test():

        res = test_task.apply_async()
        return {
            "code": 0,
            "msg": "好耶",
            "data": str(res)
        }

    @staticmethod
    @file_api.route("test_redis")
    def test_redis():
        res = redis_client.get("k")
        return str(res)
