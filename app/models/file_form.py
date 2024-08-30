from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms.fields.simple import SubmitField, StringField
from wtforms.validators import DataRequired, Length


class UploadForm(FlaskForm):
    # flask_WTF中提供的上传字段，label仍是字段的标签
    # validators接收的验证列表中：
    # FileRequired()用于验证是否包含文件对象，可以设置参数message
    # FileAllowed()用于验证文件的类型（后缀名），参数一为允许的文件后缀名的列表，参数二为可选的message
    file = FileField(label='Upload File', validators=[FileRequired(message='upload file')])
    # 采用了wtforms提供的提交字段,flask_WTF中似乎不包含该字段
    submit = SubmitField()


class RenameForm(FlaskForm):
    old_name = StringField('old_name', validators=[DataRequired(message='不能为空'), Length(min=2, max=50)])
    new_name = StringField('new_name', validators=[DataRequired(message='不能为空'), Length(min=2, max=50)])
    submit = SubmitField()


class DeleteForm(FlaskForm):
    file_name = StringField('file_name', validators=[DataRequired(message='不能为空'), Length(min=2, max=50)])
    submit = SubmitField()
