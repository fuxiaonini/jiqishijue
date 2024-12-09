import os
import cv2
import numpy as np

def get_arrays_and_ids(path="person_dir"):
    face_samples = []
    ids = []
    for i in os.listdir(path):
        if os.listdir(f"{path}/{i}") != []:
            for j in os.listdir(f"{path}/{i}"):
                img = cv2.imread(f"{path}/{i}/{j}", flags=cv2.IMREAD_GRAYSCALE)
                face_samples.append(img)
                ids.append(int(i))
        else:
            pass
    return face_samples, ids

def train_model(path="person_dir"):
    face_samples, ids = get_arrays_and_ids(path)
    is_trained = 0
    if ids != []:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.train(face_samples, np.array(ids))
        recognizer.save("model/trainer.yml")
        is_trained = 1
    else:
        pass
    return is_trained

if __name__=="__main__":
    train_model()