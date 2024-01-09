This project is further develop of group project done for West Pomeranian University of Technology, as my Engineering Thesis.

This software implements few diffrent virtual keyboards with posibility to use it in research.

Software uses Python 3.9.7.
To run it you will need webcam and mentioned libraries installed:
-numpy
-opencv
-time
-string
-collections
-threading
-mediapipe
-PyQt5
-sys
-screeninfo
-pandas
-requests
-os
-Levenshtein
-textdistance
-matplotlib

To use this software you need programming editor for Python, such as Visual Studio Code.
If you are not using laptop with built in webcam you may need to change value from 0 to 1 in front->components->Launcher.py "cap = cv2.VideoCapture(0)" (line 21).
You need to open main folder of project in editor and run main.py.

Files included in project:

- File main.py - a script launching the program.
- File stats.csv - file containing statistics produced by tests done by user
- File stats.png - file generated after user completes test, contains statistics of all records contained in "stats.csv". Represents on graph: Levenshtein, Ratcliff, Jaro Winkler, text typed by user and method used.
- File statsTime.png - file generated after user completes test, contains statistics of all records contained in "stats.csv". Represents time of finished tests and text typed by user with method used.
- Directory back:

  -Directory modules:
  
    - File FaceMeshModule.py - responsible for tracking points distributed on the face in the form of a mesh (a grid of several dozen points).
    - File FaceTrackingModule.py - responsible for tracking several key points distributed on the face.
    - File HandTrackingModule.py - responsible for tracking key points distributed on the hands.
    - File EightPen.py - responsible for the logic of the 8Pen keyboard.
    - File EpKeyboard.py - responsible for drawing the 8Pen keyboard on the camera preview screen.
    - File HandMovingKeyboard.py - responsible for the logic of a dynamic Swipe-type keyboard operated by hand.
    - File HandMovingKeyboardStatic.py - responsible for the logic of a static Swipe-type keyboard operated by hand.      
    - File HeadMovingKeyboard.py - responsible for the logic of a dynamic Swipe-type keyboard operated by head.      
    - File HeadMovingKeyboardStatic.py - responsible for the logic of a static Swipe-type keyboard operated by head.      
    - File Hover.py - responsible for the logic of a Hover-type keyboard operated by hand.      
    - File Keyboard.py - responsible for drawing Swipe and Hover type keyboards on the camera preview screen.      
    - File QWERTY.py - responsible for the logic of a QWERTY keyboard.      
    - File QWERTYKeyboard.py - responsible for drawing the QWERTY keyboard on the camera preview screen.
    - File QWERTYTile.py - responsilbe for logic of method QWERTYTile
    - File QWERTYHierarchic.py - responsible for logic of method QWERTYHierarchic
      
- Directory front:
  
  - Directory cameraView:

    - File CameraView.py - responsible for the main layout of the program - camera view + lines of text to be entered on our keyboards + lines of text entered by our keyboards + buttons for confirming and resetting the entered text + a button for               generating random Lorem Ipsum text - this file is only responsible for drawing it on the GUI screen.

- Directory components:

   - File Launcher.py - responsible for launching a side thread that searches for our camera and starts it using OpenCV, then based on user-selected data in the GUI, it launches the appropriate keyboard (draws it on the screen and imposes the                  appropriate logic).

  - File StyleSheet.py - responsible for the style of individual components in our GUI (simple CSS).
  
  - File Title.py - responsible for the component that displays the title in the upper left corner of the GUI screen.

- Directory navbar:

  - File navbar.py - responsible for the component that displays navigation on the left side of the GUI screen and its logic.

- Directory assets - contains GIF, PNG, JPG files needed for the proper display of the GUI.
