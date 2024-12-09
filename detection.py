import cv2

def detector(img, face_cascade):
    face_detector = cv2.CascadeClassifier(face_cascade)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(img_gray)

    a = 0
    b = 0
    [x, y, w, h] = [0, 0, 0, 0]
    if len(faces) != 0:
        for i, face in enumerate(faces):
            if face[3] > a:
                a = face[3]
                b = i

        [x, y, w, h] = faces[b]
        cv2.rectangle(
            img,
            (x, y), # 左上角
            (x+w, y+h), # 右下角
            color=(0, 255, 0),
            thickness=2,
        )
    return img, img_gray, [x, y, w, h]


if __name__=="__main__":
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        ret, img = cap.read()
        img, img_gray, [x, y, w, h] = detector(img, r"model/haarcascade_frontalface_default.xml")
        cv2.imshow("camere_1", img)
        cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()
