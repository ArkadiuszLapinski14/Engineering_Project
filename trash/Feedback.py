# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 13:19:19 2023

@author: Ola
"""

#Detection usage Feedback module
import pandas as pd
import os.path
import csv
import cv2
import mediapipe as mp
import time
import Modules.HandTrackingModule as htm
from keyboards_back.Keyboard import Keyboard
from keyboards_back.HandMovingKeyboard import HandMovingKeyboard

import PyQt5.QtWidgets as pq
from PyQt5 import QtGui as qtgui
from PyQt5.QtGui import QPixmap, QColor

class Feedback():

    

    def __init__(self, text_to_write, text_written):
        self.text_to_write =  (''.join(text_written)).lower()
        self.text_written = (''.join(text_written)).lower()
        print(self.text_to_write, text_written)
        
        self.app = pq.QApplication([])
        self.window = pq.QWidget()
        self.window.setWindowTitle("Hand Tracking Program Feedback")
        
        self.window.setFixedSize(550,900) 
        self.layout = pq.QVBoxLayout()
        self.grid = pq.QGridLayout()
        
            #label
        self.fatigueLabel= pq.QLabel("Choose your level of fatigue:")
        self.grid.addWidget(self.fatigueLabel, 1, 0,1,1)
       
        #COMBOBOX FATIGUE
        self.comboFatigue = pq.QComboBox()
        self.comboFatigue.setGeometry(200, 150, 120, 30)
        self.comboFatigue.addItem("Low")
        self.comboFatigue.addItem("Medium")
        self.comboFatigue.addItem("High")
        self.comboFatigue.activated[str].connect(self.get_fatigue)

        
        self.grid.addWidget(self.comboFatigue, 2, 0,1,1)
        #label
        self.futureLabel= pq.QLabel("Would you use the app again in the future?")
        self.grid.addWidget(self.futureLabel, 5, 0,1,1)
       
            #text line
        self.futureText = pq.QLineEdit()
        self.grid.addWidget(self.futureText, 6, 0,1,1)
        #print(self.futureText.text())
                    #label
        self.ageLabel= pq.QLabel("Type your age:")
        self.grid.addWidget(self.ageLabel, 7, 0,1,1)
       
            #text line
        self.ageText = pq.QLineEdit()
        self.grid.addWidget(self.ageText, 8, 0,1,1)
        #print(self.ageText.text())


         #button saving feedback file
        self.buttonSaveFeedback = pq.QPushButton("Save the feedback.")
        self.grid.addWidget(self.buttonSaveFeedback, 10, 0,1,1)
        self.buttonSaveFeedback.clicked.connect( self.save_feedback) #metoda generujaca text 
        #Setting the layout
        self.window.setLayout(self.grid)

        #Showing and executing the main window
        self.window.show()
        self.app.exec_()

    def get_fatigue(self):
        self.fatigue_level = self.comboFatigue.currentText()
     
    def check_correction(self):
        correct = 0
        for idx, el in enumerate(self.text_to_write):
            if el == self.text_written[idx]:
                correct += 1
            else:
                continue
        return (correct / len(self.text_to_write)) * 100

    def save_feedback(self):
       self.correction = self.check_correction()
       self.age = self.ageText.text()
       self.recommendation = self.futureText.text()
       self.get_fatigue()

       df = pd.DataFrame({
            'Fatigue Level': [self.fatigue_level],
            'Future Usage': [self.recommendation],
            'Age': [self.age],
            'Correction':[str(self.correction) + "%"]
        })

       if (os.path.exists('feedback.csv')):
            df.to_csv('feedback.csv', mode='a', index=False, sep=';', header=False)
       else:
            df.to_csv('feedback.csv', index=False, sep=';')


def main():

    F = Feedback()
    

if __name__ == '__main__':
    main()
    