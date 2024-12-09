import os
import cv2

def make_dir(dir_name):
    check_start = 0
    if os.path.exists(f"person_dir/{dir_name}") == False:
        os.mkdir(f"person_dir/{dir_name}")
    else:
        pass
    return check_start

def make_pic(img_gray,face_tacle,pic_name="pic_1.png"):
    [x, y, w, h] = face_tacle
    img_cut = img_gray[y:y+h, x:x+w]
    cv2.imwrite(pic_name, img_cut)

def make_little_gray(img_gray, face_tacle):
    [x, y, w, h] = face_tacle
    img_cut = img_gray[y:y+h, x:x+w]
    return img_cut

