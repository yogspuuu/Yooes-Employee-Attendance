from email.mime import image
import os
import cv2
import numpy as np
from PIL import Image
from api import UPLOAD_FOLDER
from api.recognition.models import User


def cascade_path():
    global faceCascadePath, eyeCascadePath

    # face cascade path
    faceCascadePath = f'{os.getcwd()}/utils/haarcascade_frontalface_default.xml'

    # eye cascade path
    eyeCascadePath = f'{os.getcwd()}/utils/haarcascade_eye_tree_eyeglasses.xml'


def do_recognition(video_name: str) -> str:
    # call cascade path
    cascade_path()

    # video directory
    video_path = os.path.join(UPLOAD_FOLDER, video_name)

    # read video
    capture = cv2.VideoCapture(video_path)

    # do recognition
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('models/model.yml')

    # face cascade
    faceCascade = cv2.CascadeClassifier(faceCascadePath)

    # eye cascade path
    eyeCascade = cv2.CascadeClassifier(eyeCascadePath)

    # iniciate id counter
    id = 0

    # variable store execution state
    already_blink = False

    # Define min window size to be recognized as a face
    minW = 0.1*640
    minH = 0.1*480

    while (capture.isOpened()):
        # capture video
        _, video = capture.read()

        # change video color
        gray = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY)

        # face cascade detect multi scale
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )

        for(x, y, w, h) in faces:
            id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

            # check if confidence is less them 100 ==> "0" is perfect match
            if (confidence < 100):
                confidence = "  {0}%".format(round(100 - confidence))

                # eyes cascade detect multi scale
                eyes = eyeCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.2,
                    minNeighbors=5,
                    minSize=(int(minW), int(minH)),
                )

                # check if eyes detected
                if(len(eyes) >= 2):
                    if already_blink:
                        already_blink = False
                    else:
                        if not already_blink:
                            already_blink = True
            else:
                id = None
                confidence = "{0}%".format(round(100 - confidence))

        # break while video is already read
        break

    # check if user is null or blink is false and return message
    if (id == None or already_blink == False):
        name = None
        message = "Face validation failed."
    else:
        # do query to get names
        user_query = User.query.filter_by(id=id).first()
        if not user_query:
            name = None
            message = "Failed to find user related with this face."
        else:
            name = user_query.name

    # if id user is not null or blink is not false return this messages
    message = "Succesfully detect face."

    # return collected data
    return {
        "user": name,
        "blink": already_blink,
        "messages": message
    }


def do_generate_datasets(id: int, name: str, video_name: str) -> str:
    # call cascade path
    cascade_path()

    # datasets directory
    dataset_path = f'{os.getcwd()}/datasets'

    # video directory
    video_path = os.path.join(UPLOAD_FOLDER, video_name)

    # read video
    capture = cv2.VideoCapture(video_path)

    # initialized name for classified images name
    face_id = id

    # face detector using cacade clasifier
    face_detector = cv2.CascadeClassifier(
        faceCascadePath
    )

    # initalize iamges count
    count = 0

    while (capture.isOpened()):
        if (count == 30):
            message = "Face successfully registered."
            break
        else:
            message = "Failed to registered face"

        _, video = capture.read()
        gray = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            # crop image when face detected
            cv2.rectangle(video, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # incrase count by 1
            count += 1

            # save the captured image into the datasets folder
            cv2.imwrite(
                f'{dataset_path}/.{str(face_id)}.{str(count)}.jpg', gray[y:y+h, x:x+w])

    # generate models when registering faces
    do_generate_models(dataset_path, face_id)

    # return collected data
    return {
        'name': name,
        'messages': message
    }


def do_generate_models(image_path: str, face_id: str) -> str:
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(
        faceCascadePath
    )

    def get_images_and_labels(image_path: str, face_id: str) -> str:
        imagePaths = [os.path.join(image_path, f) for f in os.listdir(image_path)]
        faceSamples = []
        ids = []

        for imagePath in imagePaths:
            PIL_img = Image.open(imagePath).convert('L')
            img_numpy = np.array(PIL_img, 'uint8')

            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = detector.detectMultiScale(img_numpy)

            for (x, y, w, h) in faces:
                faceSamples.append(img_numpy[y:y+h, x:x+w])
                ids.append(id)

        return faceSamples, ids
    
    faces, ids = get_images_and_labels(image_path, face_id)
    recognizer.train(faces, np.array(ids))

    # Save the model into models/model.yml
    # recognizer.save() worked on Mac, but not on Pi
    recognizer.write('models/model.yml')
