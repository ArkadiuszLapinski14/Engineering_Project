import cv2
import mediapipe as mp
import numpy as np
import threading
from keyboards_back.Keyboard import Keyboard

class HeadMovingKeyboard:
    def __init__(self, keyboard=Keyboard()):
        self.angles = []
        self.keyboard = keyboard
        self.keys = keyboard.get_keys()
        self.KEYS = keyboard.get_keys()
        self.res = []
        self.is_calibrated = False
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        self.classic_keyboard = Keyboard()
        self.interval = 5  # Określony czas (w sekundach)
        self.timer = None

    def update(self, img, keyboard = Keyboard()):

        img_h, img_w, img_c = img.shape
        face_3d = []
        face_2d = []
        results = self.face_mesh.process(img)
        angles2 = np.zeros(2)

        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                for idx, lm in enumerate(face_landmarks.landmark):
                    if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                        if idx == 1:
                            nose_2d = (lm.x * img_w, lm.y * img_h)
                            nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)

                        x, y = int(lm.x * img_w), int(lm.y * img_h)

                        # Get the 2D Coordinates
                        face_2d.append([x, y])

                        # Get the 3D Coordinates
                        face_3d.append([x, y, lm.z])       
            
                # Convert it to the NumPy array
                face_2d = np.array(face_2d, dtype=np.float64)

                # Convert it to the NumPy array
                face_3d = np.array(face_3d, dtype=np.float64)

                # The camera matrix
                focal_length = 1 * img_w

                cam_matrix = np.array([ [focal_length, 0, img_h / 2],
                                        [0, focal_length, img_w / 2],
                                        [0, 0, 1]])

                # The distortion parameters
                dist_matrix = np.zeros((4, 1), dtype=np.float64)

                # Solve PnP
                success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

                # Get rotational matrix
                rmat, jac = cv2.Rodrigues(rot_vec)

                # Get angles
                angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

                # Get the y rotation degree
                x = angles[0] * 360
                y = angles[1] * 360
                z = angles[2] * 360

                angles2 = [x, y]

                self.angles=angles2
        #cv2.putText(img, str(angles2[0]), (600, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
        #cv2.putText(img, str(angles2[1]), (600, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
        return(self.update2(img),self.res)
       
        
    def update2(self, screen):
        #try:
            screen = self.keyboard.draw_update(screen, 10, 100, 30, 30)
            self.headUpdate()
           # screen = self.backToDefault(screen)
            if self.is_calibrated == True:
                if len(self.keys) != 2:
                        self.cutBy4()
                elif len(self.keys) == 2:
                        self.cutBy2()
                screen = self.drawResult(screen, 600, 600)
                #return screen
            else:
                screen = self.calibrate(screen)
                screen = self.drawResult(screen, 600, 600)
            return screen 
        #except:
            #print("Head Moving Keyboard algorith doesnt work/lms out of range")
            #return screen
       

    def calibrate(self, screen):
        try:
            if (self.angles):
                if ((self.angles[1] > -5 and self.angles[1] < 5) and (self.angles[0] > -5 and self.angles[0] <5)):
                    #screen = self.CalibrationLoading(screen, x, y, w, h)
                    self.is_calibrated = True
               
   

        except:
            print("Calibration doesnt work")
        return screen


    def startTimer(self):
        self.timer = threading.Timer(self.interval, self._execute)
        self.timer.start()

    def _execute(self):
        self.keys = self.KEYS
        self.keyboard.set_keys(self.KEYS)
        
        # Uruchom ponownie timer, aby funkcja wywołała się ponownie po kolejnym interwale
        self.startTimer()
    
    def setResult(self, res):
        '''Append the result by the letter we picked or delete last of them, then set a keyboard to default values'''
        ###Usuwanie
        if res == "<":
            if len(self.res) > 0:
                del self.res[-1]
        elif res == "_":
            self.res.append(" ")
        ###Dodawanie
        else:
            self.res.append(res)

        self.keys = self.KEYS
        self.keyboard.set_keys(self.KEYS)

    def drawResult(self, screen, x, y):
        '''Draws a result on the screen'''
        screen, x, y = self.drawResultBox(screen)
        for el in self.res:
            cv2.putText(screen, el, (x,y), cv2.FONT_HERSHEY_PLAIN, 3 ,(255,255,255), 2)
            x += 30
        return screen

    def drawResultBox(self, screen):
        y, x , c = screen.shape
        x = int((x - 400)/2)
        y = int((y - 200))
        screen = cv2.rectangle(screen, (x, y), (x + 400, y + 40), (255,255,255), 2)
        return screen, x, y + 37

    def centerCoo(self, screen, w, h):
        '''return x, y at the center of the screen, based on width and height of your shape'''
        y, x, c = screen.shape
        w, h = 100, 100
        y, x = int((y-h)/2), int((x-w)/2)
        return x, y, w, h

    def headUpdate(self):
            if len(self.keys) == 1:
                self.setResult(self.keys[0])




    def cutBy4(self):
        '''Cut unecessary part of keyboard when len(keayboard) > 2'''
        try:
            if (self.angles and self.is_calibrated==True):
                if self.angles[1] <  -5 and self.angles[0]<8 and self.angles[0]>-8: 
                    self.keys = self.keys[0:int(len(self.keys)/4)]
                    self.keyboard.set_keys(self.keys)
                    self.is_calibrated = False
                    self.startTimer()
                  
                elif self.angles[1] > 5 and self.angles[0]<8 and self.angles[0]>-8:
                    self.keys = self.keys[int(len(self.keys)*(3/4)):len(self.keys)]
                    self.keyboard.set_keys(self.keys)
                    self.is_calibrated = False
                    self.startTimer()
                   
                elif self.angles[0] < -5 and self.angles[1]<8 and self.angles[1]>-8:
                    self.keys = self.keys[int(len(self.keys)*(1/4)):int(len(self.keys)*(2/4))]
                    self.keyboard.set_keys(self.keys)
                    self.is_calibrated = False
                    self.startTimer()
                    
                elif self.angles[0] > 5 and self.angles[1]<8 and self.angles[1]>-8:
                    self.keys = self.keys[int(len(self.keys)*(2/4)):int(len(self.keys)*(3/4))]
                    self.keyboard.set_keys(self.keys)
                    self.is_calibrated = False
                    self.startTimer()
                    
        except:
            print("Cut by 3/4 doesnt work/Fingers lists out of range")  

    def cutBy2(self):
        '''Cut unecessary part of keyboard when len(keayboard) == 2'''
        try:
            if (self.angles and self.is_calibrated==True):
                if self.angles[1] < - 6:
                    self.keys = self.keys[0:1]
                    self.keyboard.set_keys(self.keys)
                    self.is_calibrated = False
                    self.startTimer()
                  
                elif self.angles[1] >  6:
                    self.keys = self.keys[1:2]
                    self.keyboard.set_keys(self.keys)
                    self.is_calibrated = False
                    self.startTimer()
                  
        except:
            print("Final cut by 1/2 doesnt work/Fingers lists out of range")
