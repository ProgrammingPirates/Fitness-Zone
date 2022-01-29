import cv2,os
import mediapipe as mp
import numpy as np
import time
import gtts as gTTS
#mp_drawing = mp.solutions.drawing_utils 
#mp_pose = mp.solutions.pose 

#print(mp_pose.POSE_CONNECTIONS)
#print(mp_drawing.DrawingSpec??)
  
#print(len(landmarks)) -> no. of landmark availabe
#print(landmark) -> for current position
#for lndmark i nn mp_pose.Poseandmark:
#    print(lndmark) -> print landmark in order

#landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value] -> current position(x,y,z,visibility)
#NOSE;RIGTH_WIRST
#mp_pose.PoseLandmark.LEFT_SHOULDER.value -> 11th position

#FOR FINDING ANGLE
#landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value] 
#landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value] 
#landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]
 
#print(time.time())
#start=time.time()
#a=input()
#b="super"
#b+=str(7)
#print(b)
#end=time.time()
#print(start)
#print(end)
#end=(end-start)/60
#print(end)

myText = "1"
language = 'en'
output = gTTS(text=myText, lang=language,slow=False)
output.save("output.mp3")
os.system("start output.mp3")