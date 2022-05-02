import json
from api import db, app
from flask.views import MethodView
from api.recognition.models import User
from flask import request, jsonify, Blueprint, abort

recognition = Blueprint('recognition', __name__)


@recognition.route('/')
def home():
    return "Yooes recognition api."


class RegisterUserFaces(MethodView):
    def get(self, id):
        # Get the record for the provided id.
        return

    def post(self):
        name = request.form.get('name')
        user = User(name)
        db.session.add(user)
        db.session.commit()
        
        return jsonify({user.id: {
            'name': user.name,
        }})

    def put(self, id):
        # Update the record for the provided id
        # with the details provided.
        return

    def delete(self, id):
        # Delete the record for the provided id.
        return


class ValidateUserFaces(MethodView):
    def get(self, id=None):
        user = User.query.filter_by(id=id).first()
        if not user:
            abort(404)
        res = {
            'name': user.name,
        }
        return jsonify(res)

    def post(self, id):
        # Post the record for the provided id.
        return

    def put(self, id):
        # Update the record for the provided id
        # with the details provided.
        return

    def delete(self, id):
        # Delete the record for the provided id.
        return


register_faces = RegisterUserFaces.as_view('register_faces')
valdiate_vaces = ValidateUserFaces.as_view('valdiate_vaces')

app.add_url_rule(
    '/recognition/register/faces', view_func=register_faces, methods=['POST']
)
app.add_url_rule(
    '/recognition/validate/faces/<int:id>', view_func=valdiate_vaces, methods=['GET']
)
