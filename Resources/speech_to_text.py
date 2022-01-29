import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("Speek : ")
    audio = r.listen(source)
    try:
        text=r.recognize_google(audio)
        print(text)
    except:
        print("Can't recognize voice")