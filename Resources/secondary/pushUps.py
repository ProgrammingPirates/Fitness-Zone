import cv2
import mediapipe as mp
import numpy as np
from gtts import gTTS
from gtts import gTTS
import speech_recognition as sr
import os

cal=0
def pushup():
    text=""
    language = 'en'
    myText = "start doing pushups, say stop for ending exercise"
    language = 'en' #'fr' -> french
    output = gTTS(text=myText, lang=language,slow=False)

    output.save("output.mp3")
    os.system("start output.mp3")
    
    counter = 0
    stage = None

    def calculate_angle(a,b,c):
        a=np.array(a)
        b=np.array(b)
        c=np.array(c)
        
        radians = np.arctan2(c[1]-b[1],c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        
        if angle > 180.0:
            angle = 360-angle
        
        return angle

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    cap = cv2.VideoCapture(0)
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose :
        
        while cap.isOpened():
            ret, frame = cap.read()
            
            image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = pose.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            try:
                landmarks = results.pose_landmarks.landmark 
                
                shoulder=[landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow=[landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist=[landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                angle = calculate_angle(shoulder, elbow, wrist)
                
                r_shoulder=[landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                r_elbow=[landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                r_wrist=[landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                r_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)
                
                cv2.putText(image,str(angle), tuple(np.multiply(elbow,[640,480]).astype(int))
                            ,cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255), 2,cv2.LINE_AA )
                #cv2.putText(image,str(r_angle), tuple(np.multiply(r_knee,[640,480]).astype(int))
                            #,cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255), 2,cv2.LINE_AA )
                            
                if angle > 160 and r_angle > 160 :
                    stage = "up"
                if angle < 110 and r_angle < 110 and stage == "up":
                    stage = "down"
                    counter+=1
                    myText = str(counter)
                    output = gTTS(text=myText, lang=language,slow=False)
                    output.save("output.mp3")
                    os.system("start output.mp3")
            except:
                pass
            
            cv2.rectangle(image,(0,0),(225,73),(245,117,16),-1)
            
            cv2.putText(image, 'REPS', (15,20),
                        cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA)
            cv2.putText(image, str(counter), (10,60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
            
            cv2.putText(image, 'STAGE', (65,20),
                        cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA)
            cv2.putText(image, stage , (65,45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
            
            mp_drawing.draw_landmarks(image,results.pose_landmarks,mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(162,32,240),thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(255,255,255),thickness=2, circle_radius=2));
            
            
            cv2.imshow('PUSHUPS',image)
            
            r = sr.Recognizer()
            with sr.Microphone() as source:
                audio = r.listen(source)
                try:
                    text=r.recognize_google(audio)
                except:
                    pass
            if(text=="stop"):
                cap.release() #relese web cam
                cv2.destroyAllWindows() #close the window
                return counter*0.4
            
            if cv2.waitKey(10) & 0xFF == ord('q'): 
                break

    cap.release() 
    cv2.destroyAllWindows()
    
a=pushup();