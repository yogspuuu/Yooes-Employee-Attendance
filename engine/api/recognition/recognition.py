import os
import cv2
from api import UPLOAD_FOLDER

def do_recognition(image_name):
    # image directory
    image_path = os.path.join(UPLOAD_FOLDER, image_name)
    
    # do recognition
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('models/model.yml')
    cascadePath = f'{os.getcwd()}/utils/haarcascade_frontalface_default.xml'
    faceCascade = cv2.CascadeClassifier(cascadePath)

    # iniciate id counter
    id = 0

    # names related to ids: example ==> Marcelo: id=1,  etc
    names = ['None', 'Yoga', 'Naghita', 'Ilza', 'Z', 'W']

    # Define min window size to be recognized as a face
    minW = 0.1*640
    minH = 0.1*480

    img = cv2.imread(image_path, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )

    for(x, y, w, h) in faces:
        id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

        # Check if confidence is less them 100 ==> "0" is perfect match
        if (confidence < 100):
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
    
    return id
