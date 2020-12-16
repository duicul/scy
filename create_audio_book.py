import pyttsx3
import PyPDF2
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import os 
text = extract_pages("D:/001 [notes] GTAYQ_L1_072919_gpod101.pdf")

speaker = pyttsx3.init()  # initialization
speaker.setProperty("rate", 150)  # set speaking speed

voices = speaker.getProperty('voices') 
os.mkdir("D:/pages")
for voice in voices: 
    # to get the info. about various voices in our PC  
    print("Voice:") 
    print("ID: %s" %voice.id) 
    print("Name: %s" %voice.name) 
    print("Age: %s" %voice.age) 
    print("Gender: %s" %voice.gender) 
    print("Languages Known: %s" %voice.languages) 

speaker.setProperty('voice', voices[0].id) 
page_num = 0 
for page in text:
    print("Current page: ", page_num + 1)
    page_num+=1
    print(page)
    # print(text)
    page_text=""
    for element in page:
        if isinstance(element, LTTextContainer):
            print(element.get_text())
            page_text+=element.get_text()
    speaker.save_to_file(page_text, "D:\pages\page"+str(page_num)+".wav")
    #speaker.say(text)  # now extract text will passed here to listen
    speaker.runAndWait()
