from api import db, app
from flask.views import MethodView
from api.recognition.models import User
from flask import request, jsonify, Blueprint
from api.recognition.utils import b64_to_video
from api.recognition.engine import do_recognition
from api.recognition.engine import do_generate_datasets

recognition = Blueprint('recognition', __name__)


@recognition.route('/')
def home():
    return "Yooes recognition api."


class RegisterUserFaces(MethodView):
    def get(self, id=None):
        # Get the record for the provided id.
        return

    def post(self, id=None):
        name = request.form.get('name')

        # save name into database
        user = User(name)
        db.session.add(user)
        db.session.commit()

        # get requested base64 image data
        base64_video = request.form.get('base64_video')

        # convert base64 to image
        video = b64_to_video(base64_video)

        # show result of prediction
        result_of_capture = do_generate_datasets(user.id, user.name, video)

        return jsonify({
            'data': result_of_capture
        })

    def put(self, id=None):
        # Update the record for the provided id
        # with the details provided.
        return

    def delete(self, id=None):
        # Delete the record for the provided id.
        return


class ValidateUserFaces(MethodView):
    def get(self, id=None):
        # Get the record for the provided id.
        return

    def post(self, id=None):
        # get requested base64 image data
        base64_video = request.form.get('base64_video')

        # convert base64 to image
        video = b64_to_video(base64_video)

        # show result of prediction
        result_of_prediction = do_recognition(video)

        return jsonify({
            'data': result_of_prediction,
        })

    def put(self, id=None):
        # Update the record for the provided id
        # with the details provided.
        return

    def delete(self, id=None):
        # Delete the record for the provided id.
        return


register_faces = RegisterUserFaces.as_view('register_faces')
valdiate_faces = ValidateUserFaces.as_view('valdiate_vaces')

app.add_url_rule(
    '/recognition/register/faces', view_func=register_faces, methods=['POST']
)
app.add_url_rule(
    '/recognition/validate/faces', view_func=valdiate_faces, methods=['POST']
)
