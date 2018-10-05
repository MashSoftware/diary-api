from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models, errors

from .views.user import user
from .views.child import child
from .views.event import event
from .views.auth import auth
app.register_blueprint(user, url_prefix='/v1/users')
app.register_blueprint(child, url_prefix='/v1/children')
app.register_blueprint(event, url_prefix='/v1/events')
app.register_blueprint(auth, url_prefix='/v1/auth')
