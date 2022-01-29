import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import speech_recognition as sr
import os
from threading import Thread
from gtts import gTTS
import asyncio

tts = pyttsx3.init()
tts.setProperty("rate", 125)

def count_voice(counter):
    output = gTTS(text=str(counter[0]), lang='en',slow=False)
    output.save("output.mp3")
    os.system("start output.mp3")

def count(counter):
    t5 = Thread(target=count_voice,args=(counter,))
    t5.start()

def bicepCurls(counter,cap):
    
    stage = None
    r_stage = None

    def calculate_angle(a,b,c):
        a=np.array(a)
        b=np.array(b)
        c=np.array(c)
        
        radians = np.arctan2(c[1]-b[1],c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        #1->y axis 0->x axis
        angle = np.abs(radians*180.0/np.pi)
        
        if angle > 180.0:
            angle = 360-angle
        
        return angle

    mp_drawing = mp.solutions.drawing_utils #draw detecting in screen and in open cv
    mp_pose = mp.solutions.pose #pose modal
    
     #0 is webcam number(wise id) may differ
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose :
        #higher the min_detection_confidence and min_tracking_confidence higher the accuracy
        
        while cap.isOpened():  #until open of cam
            ret, frame = cap.read() #reading feed from web cam
            #ret is bool for frame and frame is array vector captured per sec
            
            image = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB) #recolor image, to read in correct order
            image.flags.writeable = False
            
            results = pose.process(image) #mask detection, array values
            
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) #recolor to original one
            
            #to extract landmark
            try:
                landmarks = results.pose_landmarks.landmark #3rd positioning stored in array
                #will return 33 element in array represents each position
                
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
                
                #cv2.putText(image,str(angle), tuple(np.multiply(elbow,[640,480]).astype(int)),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255), 2,cv2.LINE_AA ##fontstyling line)
                #for priting angle in image, 640*480 dimension of the webcam
                
                if angle > 160 :
                    stage = "down"
                if angle < 30 and stage == "down":
                    stage = "up"
                    counter[0]+=1
                    count(counter)
                
                if r_angle > 160 :
                    r_stage = "down"
                if r_angle < 30 and r_stage == "down":
                    r_stage = "up"
                    counter[0]+=1
                    count(counter)
            except Exception as e:
                print(e)
            
            cv2.rectangle(image,(0,0),(225,73),(245,117,16),-1)
            
            cv2.putText(image, 'REPS', (15,20), #COORDIANTE
                        cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA) #DEAFULT BOX 
            cv2.putText(image, str(counter[0]), (10,60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
            #TEXT SIZE,COLOR,2-LINE WIDTH,LINE TYPE
            
            cv2.putText(image, 'LSTAGE', (65,20), #COORDIANTE
                        cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA) #DEAFULT BOX 
            cv2.putText(image, stage , (65,45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
            
            cv2.putText(image, 'RSTAGE', (150,20), #COORDIANTE
                        cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA) #DEAFULT BOX 
            cv2.putText(image, r_stage , (150,45), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1, cv2.LINE_AA)
            
            mp_drawing.draw_landmarks(image,results.pose_landmarks,mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(162,32,240),thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(255,255,255),thickness=2, circle_radius=2));
            
            cv2.imshow('BICEP CURLS',image)#console
            
            if cv2.waitKey(10) & 0xFF == ord('q'): #if we hit q then while loop while we break
                break

def speech_rec(counter):
    cap = cv2.VideoCapture(0)

    t1 = Thread(target=bicepCurls, args=(counter,cap))
    t1.start()
    text=""
    while(text!="stop"):
        print("speak : ")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            try:
                text=r.recognize_google(audio)
            except:
                pass
        if(text=="stop"):
            print(counter[0]*0.01)
            cap.release() #relese web cam
            cv2.destroyAllWindows() #close the window
            break
            # return counter[0]*0.03
            
        print("stop");

def main():
    counter=[0]

    myText = "start doing bicepcurls, say stop for ending exercise"
    tts.say(myText)
    tts.runAndWait()

    
    t2 = Thread(target=speech_rec, args=(counter,))
    
    t2.start()
    t2.join()

    print(counter[0]*0.01)

    return(counter[0]*0.01)
main()