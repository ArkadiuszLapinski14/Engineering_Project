from eightPen_class import EightPen
from eightPen_keyboard import EPGenerator
import cv2

def main():
    methode="palec"
    cap = cv2.VideoCapture(0)

    ep=EightPen(methode)
    gen=EPGenerator()

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = ep.update(img,gen)
        cv2.imshow("Image", img)
        cv2.waitKey(1) #DO UZGODNIENIA


main()