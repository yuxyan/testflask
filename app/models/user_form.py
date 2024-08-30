from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class UserForm(FlaskForm):
    username = StringField(label='用户名：', validators=[DataRequired(message='用户名不能为空'), Length(min=2, max=50)])
    password = PasswordField(label='密码：', validators=[DataRequired(message='密码不能为空')])
    submit = SubmitField(label='提交')


class UserRegisterForm(FlaskForm):
    # 定义表单中的元素，类似于html的form中定义input标签下的内容
    # label 用于点击后跳转到某一个指定的field框
    # validators 用于接收一个验证操作列表
    # render_kw 用于给表单字段添加属性，各属性以键值对的形式设置
    username = StringField(label='用户名:',
                           validators=[DataRequired(message=u'用户名不能为空'),
                                       Length(2, 50, message='长度位于2~50之间')],
                           render_kw={'placeholder': '输入用户名'})
    # message中存放判断为错误时要返回的信息，EqualTo中第一个参数是要比较的field组件
    password = PasswordField(label='密码:',
                             validators=[DataRequired(message=u'密码不能为空'),
                                         EqualTo('password2', message=u'两次输入需相同')],
                             render_kw={'placeholder': '输入密码'})
    password2 = PasswordField(label='再次输入密码:',
                              validators=[DataRequired(message=u'密码不能为空')],
                              render_kw={'placeholder': '再次输入密码'})
    submit = SubmitField(label='提交')
