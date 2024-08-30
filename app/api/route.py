from flask import Blueprint
from app.api.user_api import user_api
from app.api.file_api import file_api
from app.api.label_api import label_api

route = Blueprint('api', __name__)

route.register_blueprint(user_api, url_prefix='/user')
route.register_blueprint(file_api, url_prefix='/file')
route.register_blueprint(label_api, url_prefix='/label')