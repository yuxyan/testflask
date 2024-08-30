from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from .core.exts import jwt
from app.api.route import route


app = Flask(__name__)
app.config["SECRET_KEY"] = "226790535ebee0623ce62dc8bfe3ce27eafef15040011414f3dd3aa1e7ad15de"
app.config["CSRF_ENABLED"] = True

csrf = CSRFProtect(app)

jwt.init_app(app)
app.register_blueprint(route)

app.run(debug=True)
