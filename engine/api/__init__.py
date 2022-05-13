import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Config for upload files   
UPLOAD_FOLDER = f'{os.getcwd()}/../storage/app/recognition_video'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
# def allowed_file(filename):
#     return '.' in filename and \
#         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Config for database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../yooes.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Config for blueprint
from api.recognition.views import recognition
app.register_blueprint(recognition)
db.create_all()
