from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../yooes.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from api.recognition.views import recognition
app.register_blueprint(recognition)

db.create_all()
