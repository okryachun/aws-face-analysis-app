from tensorflow.keras.models import model_from_json
import numpy as np
import tarfile
import cv2
import sys
import os

class FaceNotFound(Exception):
    """Thrown when a face is not found on camera"""
    pass


def crop_face(img):
    """Detect a face and return a cropped image singling out a face.
    
    Parameters
    ----------
        img (np.array): images numpy matrix
    Returns
    -------
        face (np.array): cropped image of a detected face
    """
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier('static/xml/haarcascade_frontalface_alt2.xml')    
        faces = face_cascade.detectMultiScale(gray, 1.05, 5)
        face = np.array(0)
        # if face found
        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            
            # extend the size of the face detected
            ext = int(abs(h-y) * 0.5)
            
            # test if extension fits on image, if not ext maximum amount
            if (y+h+ext) > img.shape[0]:
                ext = img.shape[0] - h
            face = img[y:y + h + ext, x:x + w]
            
    # if problem with extracting face, print error and raise FaceNotFound
    except Exception as e:
        print("Error1: ", e)
        raise FaceNotFound
    
    return face


def process_image(img, model_vars):
    """Resize, normalize, and expand dimensions of `img`

    Parameters
    ----------
        img (np.array): image pixel matrix 
        model_vars (dict): various variable values defined for the model
    Returns
    -------
        img (np.array): altered image pixel matrix
    """
    width = model_vars["im_width"]
    height = model_vars["im_width"]
    img = crop_face(img)
    img = cv2.resize(img, (width, height))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0)

    return img


def process_results(age, race, gender, model_vars):
    """Select argmax from predictions, map predcitions to string values

    Parameters
    ----------
        age (float): predicted age (normalized)
        race (list): predicted race categorical output list
        gender (list): predicted gender categorical output list
        max_age (int): maximum age that normalized age data
        model_vars (dict): various variable values defined for the model
    Returns
    -------
        age (str): predicted age (unnormalized)
        race (str): predicted race mapped to string value
        gender (str): predicted gender mapped to string value
    """
    max_age = model_vars["max_age"]
    age = str(round(age[0][0] * max_age))
    gender = model_vars["dataset_dict"]['gender_id'][gender.argmax()]
    race = model_vars["dataset_dict"]['race_id'][race.argmax()]
    return age, race, gender


def get_model(path):
    """Load pretrained CNN model from local directory
    
    Parameters
    -------
        path (str): path to saved json model
    Returns
    -------
        model (Model): pretrained loaded tensorflow model
    """

    model_structure_path = os.path.join(path, "model.json")
    model_weights_path = os.path.join(path, "weights.h5")        

    # untar weights file if untarred file doesn't exist
    if not os.path.exists(model_weights_path):
        tar_weights_path = model_weights_path[:-2] + "tar.gz"
        if os.path.exists(tar_weights_path):
            print(f"Extracting model weights from {tar_weights_path}.")
            tar_data = tarfile.open(tar_weights_path)
            tar_data.extractall(path)
            tar_data.close()
        else:
            print("Error: Missing model weights .h5 file.")
            sys.exit(1)    

    with open(model_structure_path, 'r') as f:
        loaded_json_model = f.read()

    model = model_from_json(loaded_json_model)
    model.load_weights(model_weights_path)
    
    return model


def get_model_vars():
    """Define variables used across this program.

    Return
    ------
        model_vars (dict): dict containing all variables and mapping dicts
    """
    # dictionary to map image attributes to string values
    dataset_dict = {
        'race_id': {
            0: 'white',
            1: 'black',
            2: 'asian',
            3: 'indian',
            4: 'others'
        },
        'gender_id': {
            0: 'male',
            1: 'female'
        }
    }

    # reverse id to alias dicts
    dataset_dict['gender_alias'] = dict((g, i) for i,
                                        g in dataset_dict['gender_id'].items())
    dataset_dict['race_alias'] = dict((r, i) for i,
                                      r in dataset_dict['race_id'].items())

    model_vars = {
        'train_split': 0.7,
        'im_width': 160,
        'im_height': 160,
        'gender_count': 2,
        'race_count': 5,
        'max_age': 116,
        'dataset_dict': dataset_dict
    }

    return model_vars


def optimize_text(text, img):
    """Adjust text font, size, location for image frame

    Parameters
    ----------
        text (str): string to be displayed on a cv2 frame
        img (np.array): img that will be displayed on frame

    Returns
    -------
        put_text (dict): optimized parameter arguments for cv2.putText
    """
    img_width, img_height, _ = img.shape
    font = cv2.FONT_HERSHEY_SIMPLEX

    scale = cv2.getFontScaleFromHeight(font, round(img_height*0.033))
    thickness = round(scale * 1.8)

    text_size = {"text": text, "fontFace": font,
                 "fontScale": scale, "thickness": thickness}

    org = cv2.getTextSize(**text_size)[0]
    
    # set padding around text
    org = (int(img_width*0.02), int(org[1]*1.3))    

    put_text = {
        "img": img,
        "text": text,
        "fontFace": font,
        "org": org,
        "fontScale": scale,
        "color": (255, 0, 0),
        "thickness": thickness,
        "lineType": cv2.LINE_AA,
        "bottomLeftOrigin": False
    }

    return put_text
