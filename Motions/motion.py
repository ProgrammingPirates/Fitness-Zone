import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils #draw detecting in screen and in open cv
mp_holistic = mp.solutions.holistic #modal


cap = cv2.VideoCapture(0) #0 is webcam number(wise id) may differ

with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic :
    #higher the min_detection_confidence and min_tracking_confidence higher the accuracy
    
    while cap.isOpened():  #until open of cam
        ret, frame = cap.read() #reading feed from web cam
        #ret is bool for frame and frame is array vector captured per sec
        
        image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) #recolor image
        results = holistic.process(image) #mask detection
        
        #print -> results.face_landmarks for face position, results.pose_landmarks for body position
        #face_landmarks, pose_landmarks, left_hand_landmarks, right_hand_landmarks 
        
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) #recolor to original one
        
        #drawing face landmarks
        mp_drawing.draw_landmarks(image,results.face_landmarks,mp_holistic.FACEMESH_CONTOURS,
                                  mp_drawing.DrawingSpec(color=(144,238,144),thickness=1, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(255,255,255),thickness=1, circle_radius=1))
        #3rd parameter has mp_holistic.FACEMESH_CONTOURS or mp_holistic.FACEMESH_TESSELATION
        #FACE_CONNECTIONS,FACEMESH_CONTOURS,FACEMESH_TESSELATION say which connects to which
        #rbg color
        
        #drawing right hand landmarks
        mp_drawing.draw_landmarks(image,results.right_hand_landmarks,mp_holistic.HAND_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(162,32,240),thickness=1, circle_radius=1),
                                  mp_drawing.DrawingSpec(color=(255,255,255),thickness=1, circle_radius=1)) 
        
        #drawing left hand landmarks
        mp_drawing.draw_landmarks(image,results.left_hand_landmarks,mp_holistic.HAND_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(162,32,240),thickness=1, circle_radius=1),
                                  mp_drawing.DrawingSpec(color=(255,255,255),thickness=1, circle_radius=1))
        
        #drawing pose landmarks -> which detect pose also
        mp_drawing.draw_landmarks(image,results.pose_landmarks,mp_holistic.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(255,182,193),thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(255,255,255),thickness=2, circle_radius=2)) 
        
        
        
        cv2.imshow('Holistic Model Detection',image)#console
        if cv2.waitKey(10) & 0xFF == ord('q'): #if we hit q then while loop while we break
            break

cap.release() #relese web cam
cv2.destroyAllWindows() #close the window