from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Test!2024@usersdb.c58judvxtxzq.us-east-1.rds.amazonaws.com:3306/users_db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
from users_app import routes
app.app_context().push()