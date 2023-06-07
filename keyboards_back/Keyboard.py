import cv2
import string

class Keyboard:
    def __init__(self, keys = list(string.ascii_uppercase + "!" + '?'+','+'.'+'<'+"_")):
        self.keys = keys
        
    def draw_update(self, screen, x, y, w, h, color = (192,192,192)):
        '''Draws a keyboard on the screen'''
        height, width, c = screen.shape
        x = int((width - (len(self.keys) * w + len(self.keys) * 2))/2)
        for idx, el in enumerate(self.keys):
            cv2.rectangle(screen, (x, y), (x + w, y + h), color, -1)
            cv2.putText(screen, el, (x + 5,y + 25), cv2.FONT_HERSHEY_PLAIN, 2 ,(255,255,255), 2)
            y = self.adjust_y(idx, y)
            x += 32
        return screen
    
    def draw_update_hover(self, screen, x, y, w, h, color=(192, 192, 192)):
        '''Draws a keyboard on the screen'''
        height, width, c = screen.shape
        x = int((width - (len(self.keys) * w + len(self.keys) * 2)) / 2)
        self.key_positions = []  # Reset the key positions
        for idx, el in enumerate(self.keys):
            cv2.rectangle(screen, (x, y), (x + w, y + h), color, -1)
            cv2.putText(screen, el, (x + 5, y + 25), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
            self.key_positions.append([(x, y), (x + w, y + h)])  # Store the key positions
            y = self.adjust_y(idx, y)
            x += 32
        return screen
    
    def highlight(self, screen, bin_tab, x, y, w, h, color = (255,160,122)):
        '''Highlights correct keys'''
        height, width, c = screen.shape
        x = int((width - (len(self.keys) * w + len(self.keys) * 2))/2)
        for idx, el in enumerate(self.keys):
            if bin_tab[idx] == 1:
                cv2.rectangle(screen, (x, y), (x + w, y + h), color, -1)
                cv2.putText(screen, el, (x + 5,y + 25), cv2.FONT_HERSHEY_PLAIN, 2 ,(255,255,255), 2)
            y = self.adjust_y(idx, y)
            x += 32
        return screen

    def adjust_y(self, idx, y):
        '''Changes y axis in order to display a "fancy keyboard"'''
        if idx == (len(self.keys)/4) - 1 and len(self.keys) > 2:
            return y + 10
        elif idx == ((len(self.keys)/4) * 2) - 1 and len(self.keys) > 2:
            return y - 20
        elif idx == ((len(self.keys)/4) * 3) -1 and len(self.keys) > 2:
            return y + 10
        else:
            return y

    def set_keys(self, keys):
        self.keys = keys

    def get_keys(self):
        return self.keys
        
    def get_key_at_position(self, position):
        '''Get the key at a given position'''
        for idx, key_position in enumerate(self.key_positions):
            if key_position[0][0] <= position[0] <= key_position[1][0] and \
                    key_position[0][1] <= position[1] <= key_position[1][1]:
                return self.keys[idx]
        return None