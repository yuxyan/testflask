from flask import Blueprint, request, abort, render_template
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.models.user_form import UserForm, UserRegisterForm
from app.service.user_service import UserService
from app.schema import user_schema
from app.core.redis import redis_client
user_api = Blueprint('user_api', __name__)


class UserApi:
    @staticmethod
    @user_api.get('/home')
    @jwt_required()
    def user():
        username = get_jwt_identity()
        return {
            "code": 0,
            "msg": "success",
            "data": username
        }

    @staticmethod
    @user_api.route('/login', methods=['POST', 'GET'])
    def login():
        form = UserForm()
        if request.method == 'GET':
            return render_template('user_login.html', form=form)
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            hash_password = UserService.hash_password(password)

            db_user = UserService.user_login(username, hash_password)
            if db_user is None:
                abort(404)
            access_token = create_access_token(identity=username)
            redis_client.hmset(db_user.username, {"username": db_user.username, "privilege": db_user.privilege,
                                                  "access_token": access_token})
            redis_client.expire(db_user.username, 1200)
            data = {
                "user": {
                    "username": db_user.username,
                    "privilege": db_user.privilege,
                },
                "access_token": access_token
            }
            return {
                "code": 0,
                "msg": "登陆成功",
                "data": data
            }
        else:
            abort(404)

    @staticmethod
    @user_api.route('/register', methods=['POST', 'GET'])
    def register():
        form = UserRegisterForm()
        if request.method == 'GET':
            return render_template('user_register.html', form=form)
        elif request.method == 'POST':
            # form.validate_on_submit() 等价于：request.method=='post' and form.validate()
            # form.validate() 用于验证表单的每个字段（控件），都满足时返回值为True
            if form.validate_on_submit():
                username = form.username.data
                password = form.password.data
                db_user = UserService.get_user(username)
                if db_user:
                    abort(409)
                hash_password = UserService.hash_password(password)
                user = user_schema.UserCreate(username=username, password=hash_password, privilege='Public')
                db_user = UserService.user_register(user)
                data = {
                    "username": db_user.username,
                    "password": db_user.password,
                    "privilege": db_user.privilege
                }
                return {
                    "code": 0,
                    "msg": "注册成功",
                    "data": data
                }
            else:
                # flask的form使用一个字典来储存各控件的errors列表
                # print(type(form.errors))
                # 输出密码字段导致validate_on_submit为false的错误原因（两种方式）
                print(form.errors['password'])
                print(form.password.errors)
                return render_template('user_register.html', form=form)


