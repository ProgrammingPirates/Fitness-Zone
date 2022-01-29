import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import speech_recognition as sr
import os
from gtts import gTTS
from threading import Thread

tts = pyttsx3.init()
tts.setProperty("rate", 125)

def count_voice(counter):
    output = gTTS(text=str(counter[0]), lang='en',slow=False)
    output.save("output.mp3")
    os.system("start output.mp3")

def count(counter):
    t5 = Thread(target=count_voice,args=(counter,))
    t5.start()

def squats(counter,cap):
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
                
                hip=[landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                knee=[landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                ankle=[landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                angle = calculate_angle(hip, knee, ankle)
                
                r_hip=[landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                r_knee=[landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                r_ankle=[landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
                r_angle = calculate_angle(hip, r_knee, r_ankle)
                
                #cv2.putText(image,str(angle), tuple(np.multiply(knee,[640,480]).astype(int))
                            #,cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255), 2,cv2.LINE_AA )
                #cv2.putText(image,str(r_angle), tuple(np.multiply(r_knee,[640,480]).astype(int))
                            #,cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255), 2,cv2.LINE_AA )
                            
                if angle > 150 and r_angle > 150 :
                    stage = "stand"
                if angle < 120 and r_angle<120 and stage == "stand":
                    stage = "sit"
                    counter[0]+=1
                    count(counter)
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
            
            
            cv2.imshow('SQUATS',image)
            if cv2.waitKey(10) & 0xFF == ord('q'): 
                break 

def speech_rec(counter):
    cap = cv2.VideoCapture(0)

    t1 = Thread(target=squats, args=(counter,cap))
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
            print(counter[0]*0.03)
            cap.release() #relese web cam
            cv2.destroyAllWindows() #close the window
            break
            
        print("stop");

def main():
    
    counter=[0]

    myText = "start doing squats, say stop for ending exercise"
    tts.say(myText)
    tts.runAndWait()

    
    t2 = Thread(target=speech_rec, args=(counter,))
    
    t2.start()
    t2.join()

    print(counter[0]*0.03)

    return(counter[0]*0.03)

main()