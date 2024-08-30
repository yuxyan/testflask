from datetime import datetime

from flask import Blueprint, request, render_template, abort
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models.label_form import LabelForm
from app.service.label_service import LabelService
from app.schema.label_schema import LabelCreate, LabelUpdate, LabelDelete

label_api = Blueprint('label_api', __name__)


class LabelAPI:
    @staticmethod
    @label_api.route('/create_labels', methods=['GET', 'POST'])
    @jwt_required()
    def create_labels():
        form = LabelForm()
        username = get_jwt_identity()
        if request.method == 'GET':
            return render_template('create_label.html', form=form)
        if form.validate_on_submit():
            label_name = form.label_name.data
            description = form.description.data
            creation_time = datetime.now()
            if LabelService.get_label(label_name) is not None:
                abort(400)
            label_create = LabelCreate(label_name=label_name, description=description, creator=username,
                                       creation_time=creation_time, is_delete=False)
            LabelService.label_create(label_create)
            data = {
                "label_name": label_name,
                "creation_time": creation_time
            }
            return {
                "code": 0,
                "msg": "成功",
                "data": data,
            }

