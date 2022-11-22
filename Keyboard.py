import cv2
import string

class Keyboard:
    def __init__(self, keys = list(string.ascii_uppercase + "." + ','+'/'+';'+'['+']')):
        self.keys = keys
        
    def draw_update(self, screen, x, y, w, h):
        '''Draws a keyboard on the screen'''
        for el in self.keys:
            cv2.rectangle(screen, (x, y), (x + w, y + h), (192,192,192), -1)
            cv2.putText(screen, el, (x + 5,y + 15), cv2.FONT_HERSHEY_PLAIN, 1 ,(255,255,255), 2)
            x += 25
        return screen

    def set_keys(self, keys):
        self.keys = keys

    def get_keys(self):
        return self.keys