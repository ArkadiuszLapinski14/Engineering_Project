import cv2
import mediapipe as mp
import numpy as np
import collections
from keyboards_back.Keyboard import Keyboard

class HeadMovingKeyboardStatic:
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
        self.keyboard_bin_tab = np.ones(32)
        self.mask = np.ones(32)

    def update(self, img):

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

                #self.angles=angles2
        #cv2.putText(img, str(angles2[0]), (600, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
        #cv2.putText(img, str(angles2[1]), (600, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
        return(self.update2(img,angles2),self.res)
       
        
    def update2(self, screen,angles):
        try:
            screen = self.keyboard.draw_update(screen, 10, 100, 30, 30)
            screen = self.keyboard.highlight(screen, self.keyboard_bin_tab, 10, 100, 30, 30)
            self.headUpdate(angles)
            if self.is_calibrated == True:
                if collections.Counter(self.keyboard_bin_tab)[1] == 32:
                    self.cutBy4()
                elif collections.Counter(self.keyboard_bin_tab)[1] == 8: 
                    self.cutBy2()
                elif collections.Counter(self.keyboard_bin_tab)[1] == 2:
                    self.cutBy1()
                screen = self.drawResult(screen, 600, 600)
                return screen
            else:
                screen = self.calibrate(screen)
                screen = self.drawResult(screen, 600, 600)
        except:
            print("Angles do not work")
        return screen 
       

    def calibrate(self, screen):
        try:
            if (self.angles):
                if ((self.angles[1] > -5 and self.angles[1] < 5) and (self.angles[0] > -5 and self.angles[0] <5)):
                    #screen = self.CalibrationLoading(screen, x, y, w, h)
                    self.is_calibrated = True
        except:
            print("Calibration doesnt work")
        return screen


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
        self.keyboard_bin_tab = np.ones(32)
        self.mask = np.ones(32)

    # def drawResult(self, screen, x, y):
    #     '''Draws a result on the screen'''
    #     screen, x, y = self.drawResultBox(screen)
    #     for el in self.res:
    #         cv2.putText(screen, el, (x,y), cv2.FONT_HERSHEY_PLAIN, 3 ,(255,255,255), 2)
    #         self.keyboard_bin_tab = np.ones(32)
    #         self.mask = np.ones(32)
    #         x += 30
    #     return screen
    def drawResult(self, screen, x, y):
        '''Draws a result on the screen'''
        screen, x, y = self.drawResultBox(screen)
        for el in self.res:
            cv2.putText(screen, el, (x,y), cv2.FONT_HERSHEY_PLAIN, 3 ,(255,255,255), 2)
            x += 30
        return screen

    def drawBackButton(self, screen):
        '''Draws button "Back"'''
        y, x , c = screen.shape
        x = int(x - 10)
        y = 10
        screen = cv2.rectangle(screen, (x, y), (x - 78, y + 25), (0, 0, 0), 3)
        screen = cv2.rectangle(screen, (x, y), (x - 78, y + 25), (192,192,192), -1)
        cv2.putText(screen, "Back", (x-78, y+23), cv2.FONT_HERSHEY_PLAIN, 2 ,(255,255,255), 2)
        return screen, x, y

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

    def headUpdate(self, angles):
        if (angles):
            self.angles = angles
            # self.angles = self.angles*360
            if len(self.keys) == 1:
                self.setResult(self.keys[0])




    def cutBy4(self):
        '''Cut unecessary part of keyboard when len(keayboard) > 2'''
        try:
            if (self.angles and self.is_calibrated==True):
                tab_len = len(self.keyboard_bin_tab)
                #down
                if self.angles[1] <  -8 and self.angles[0]<8 and self.angles[0]>-8: 
                    self.mask = np.concatenate((np.ones(int(tab_len / 4)), np.zeros(int((tab_len / 4)*3))), axis=None)
                    self.keyboard_bin_tab *= np.array(self.mask)
                    self.is_calibrated = False
                #right  
                elif self.angles[1] > 8 and self.angles[0]<8 and self.angles[0]>-8:
                    self.mask = np.concatenate((np.zeros(int((tab_len / 4) * 3)), np.ones(int(tab_len/4))), axis = None)
                    self.keyboard_bin_tab *= np.array(self.mask)
                    self.is_calibrated = False
                #left   
                elif self.angles[0] < -8 and self.angles[1]<8 and self.angles[1]>-8:
                    self.mask = np.concatenate((np.zeros(int(tab_len/4)), np.ones(int(tab_len/4)), np.zeros(int((tab_len/4) *2))), axis = None)
                    self.keyboard_bin_tab *= np.array(self.mask)
                    self.is_calibrated = False
                #up    
                elif self.angles[0] > 8 and self.angles[1]<8 and self.angles[1]>-8:
                    self.mask = np.concatenate((np.zeros(int((tab_len/4)*2)), np.ones(int(tab_len/4)), np.zeros(int(tab_len/4))), axis=None)
                    self.keyboard_bin_tab *= np.array(self.mask)
                    self.is_calibrated = False
                    
        except:
            print("Cut by 3/4 doesnt Work/angles lists out of range")  


    def cutBy2(self): ###ZNALEZC INDEKSY 1 i ZROBIC MASKA * TE INDEKSY
        '''Highlight part of keyboard'''
        try:
            tab_len = len(self.keyboard_bin_tab) 
            if (self.angles and self.is_calibrated==True):
                #left
                if self.angles[1] <  -8 and self.angles[0]<8 and self.angles[0]>-8:  
                    idxs = np.where(self.keyboard_bin_tab == 1)
                    self.keyboard_bin_tab = np.delete(self.keyboard_bin_tab, idxs, None)
                    self.mask = np.array([1,1,0,0,0,0,0,0])
                    self.keyboard_bin_tab = np.insert(self.keyboard_bin_tab, [idxs[0][0] for i in range(len(idxs))], self.mask)
                    self.is_calibrated = False
                    #down
                elif self.angles[0] < -8 and self.angles[1]<8 and self.angles[1]>-8:
                    idxs = np.where(self.keyboard_bin_tab == 1)
                    self.keyboard_bin_tab = np.delete(self.keyboard_bin_tab, idxs, None)
                    self.mask = np.array([0,0,1,1,0,0,0,0])
                    self.keyboard_bin_tab = np.insert(self.keyboard_bin_tab, [idxs[0][0] for i in range(len(idxs))], self.mask)
                    self.is_calibrated = False
                    #up
                elif self.angles[0] > 8 and self.angles[1]<8 and self.angles[1]>-8:
                    idxs = np.where(self.keyboard_bin_tab == 1)
                    self.keyboard_bin_tab = np.delete(self.keyboard_bin_tab, idxs, None)
                    self.mask = np.array([0,0,0,0,1,1,0,0])
                    self.keyboard_bin_tab = np.insert(self.keyboard_bin_tab, [idxs[0][0] for i in range(len(idxs))], self.mask)
                    self.is_calibrated = False 
                    #right
                elif self.angles[1] > 8 and self.angles[0]<8 and self.angles[0]>-8:
                    idxs = np.where(self.keyboard_bin_tab == 1)
                    self.keyboard_bin_tab = np.delete(self.keyboard_bin_tab, idxs, None)
                    self.mask = np.array([0,0,0,0,0,0,1,1])
                    self.keyboard_bin_tab = np.insert(self.keyboard_bin_tab, [idxs[0][0] for i in range(len(idxs))], self.mask)
                    self.is_calibrated = False
        except:
            print("Cut by 1/8 doesnt work/angles out of range")  
            
    def cutBy1(self):
        '''Higlight part of a keyboard and append result list of given value'''
        try:
            if self.angles[1] <  -8 and self.angles[0]<8 and self.angles[0]>-8:
                idxs = np.where(self.keyboard_bin_tab == 1)
                self.setResult(self.keys[idxs[0][0]])
                self.is_calibrated = False
            elif self.angles[1] > 8 and self.angles[0]<8 and self.angles[0]>-8:
                idxs = np.where(self.keyboard_bin_tab == 1)
                self.setResult(self.keys[idxs[0][1]])
                self.is_calibrated = False
        except:
            print("Cut by 1/16 doesnt work/angles out of range")
