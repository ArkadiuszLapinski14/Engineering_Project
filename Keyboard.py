import cv2
import string

class Keyboard:
    def __init__(self, keys = list(string.ascii_uppercase + "." + ','+'/'+';'+'['+']')):
        self.keys = keys
        
    def draw_update(self, screen, x, y, w, h):
        '''Draws a keyboard on the screen'''
        # length = len(self.keys)
        # margin = 766 - (length * w)/2
        # print(margin)
        for el in self.keys:
            cv2.rectangle(screen, (x, y), (x + w, y + h), (192,192,192), -1)
            cv2.putText(screen, el, (x + 5,y + 25), cv2.FONT_HERSHEY_PLAIN, 2 ,(255,255,255), 2)
            x += 32
        return screen

    def set_keys(self, keys):
        self.keys = keys

    def get_keys(self):
        return self.keys