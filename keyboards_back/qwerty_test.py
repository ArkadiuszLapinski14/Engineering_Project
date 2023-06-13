import cv2
from qwerty_class import QWERTY
from qwerty_keyboard import QwertyKeyboard

def main():
    methode="palec"
    img_size=(1920,1080)
    margin=20
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, img_size[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, img_size[1])

    ep=QWERTY(margin=margin)
    kboard=QwertyKeyboard()

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img, sentance = ep.update(img,keyboard=kboard)
        print(sentance)
        cv2.imshow("Image", img)
        cv2.waitKey(1) #DO UZGODNIENIA


main()
