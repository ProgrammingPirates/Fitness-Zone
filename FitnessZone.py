import pyttsx3
import mediapipe as mp
import numpy as np
import speech_recognition as sr
import cv2
import os
import time
from threading import Thread

counter=[0]

tts = pyttsx3.init()
tts.setProperty("rate", 125)

def text_to_speech(myText):
    tts.say(myText)
    tts.runAndWait()
    
def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak : ")
        audio = r.listen(source)
        try:
            text=r.recognize_google(audio)
            print(text)
            return text
        except:
            print("Can't recognize voice")
            return "Can't recognize voice"
            
def over():
    end=time.time()
    end=(end-start)
    
    print("Workout duration in min: ",end=" ")
    print(end)
    print("Burned calories : ",end=" ")
    print(counter[0])
    
    text_to_speech("Details will send to your given mobile number and email")
    if(end>1 and counter[0]!=0):
        file1 = open("user.txt","w")
        line1 = "Name : "+name+"\n"
        line2 = "Email : "+email+"\n"
        line3 = "Workout duration : "+str(end)+"\n"
        line4 = "Burned calories : "+str(cal)+"\n"
        line5 = "Telno : "+number
        file1.writelines([line1, line2, line3, line4, line5])
        file1.close()
    exit()

text_to_speech("Enter the details")

print("Enter name : ",end=" ")
name=input()
print("Enter phone number : ",end=" ")
number=input()
print("Enter email address : ",end=" ")
email=input()

text_to_speech("Welcome to Fitness Zone, Please say Start to begin workout")
#time.sleep(5)
text=""

text=speech_to_text()
if(text=="Can't recognize voice"):
    text_to_speech("Can not recognize voice please say it again")
    #time.sleep(10)
    text=speech_to_text()
    
counter[0]=0
if(text=="start"):
    
    text_to_speech("Three Workouts available Choice by saying the name and the workouts are bicep curl, pushups, squats")
    #time.sleep(10)
    
    while(text=="start"):
        start=time.time()
        if(text!="no"):
            text=speech_to_text()
        
        if(text=="bicep curls" or text=="bicep curl"):
            print("bicep curl")
            
            from bicepCurl import speech_rec
            t1 = Thread(target=speech_rec, args=(counter,))
            t1.start()
            t1.join()

            counter[0]+=counter[0]
            text="start"
            
        elif(text=="push ups" or text=="push up"):
            print("pushups")
            from pushUps import speech_rec
            t1 = Thread(target=speech_rec, args=(counter,))
            t1.start()
            t1.join()

            counter[0]+=counter[0]
            text="start"
            
        elif(text=="squats" or text=="squat"):
            print("squats")
            from squats import speech_rec
            t1 = Thread(target=speech_rec, args=(counter,))
            t1.start()
            t1.join()

            counter[0]+=counter[0]
            text="start"
        
        elif(text=="no"):
            over()
            
        else:
            text_to_speech("can't recognize voice,  say yes to do exercise no to exit")
            #time.sleep(5)
            text=speech_to_text()
            if(text=="yes"):
                text="start"
            else:
                text="no"
            
        if(text=="start"):
            text_to_speech("Say the name and the workouts are bicep curl, pushups, squats else no to exit")
            #time.sleep(10)
        
        if(text=="no"):
            over()
