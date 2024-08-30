from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class LabelForm(FlaskForm):
    label_name = StringField('label_name', validators=[DataRequired(message='不能为空'), Length(min=2, max=50)])
    description = StringField('description', validators=[Length(max=200)])
    submit = SubmitField()

