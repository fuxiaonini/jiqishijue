import cv2

def mk_recognizer():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("model/trainer.yml")
    return recognizer

def do_recognize(recognizer, img_gray_array):
    id, confidence = recognizer.predict(img_gray_array)
    return id, confidence



