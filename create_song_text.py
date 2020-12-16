import pyttsx3
import PyPDF2
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import os 
file = open("rapgod.txt","r")
text=file.read()
print(str(text))
speaker = pyttsx3.init()  # initialization
speaker.setProperty("rate", 200)  # set speaking speed
speaker.setProperty('volume', 1)
voices = speaker.getProperty('voices') 
for voice in voices: 
    # to get the info. about various voices in our PC  
    print("Voice:") 
    print("ID: %s" %voice.id) 
    print("Name: %s" %voice.name) 
    print("Age: %s" %voice.age) 
    print("Gender: %s" %voice.gender) 
    print("Languages Known: %s" %voice.languages) 

speaker.setProperty('voice', voices[0].id)
speaker.save_to_file(text, "rapgod.wav")
speaker.runAndWait()
