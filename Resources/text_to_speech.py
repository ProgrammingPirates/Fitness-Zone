from gtts import gTTS
import os

#fh = open("test.txt", "r") to read from the file
#myText = fh.read().replace("\n"," ")

myText = "starting the setup"
language = 'en' #'fr' -> french
output = gTTS(text=myText, lang=language,slow=False)

output.save("output.mp3")
os.system("start output.mp3")