import webbrowser
import speech_recognition as sr

r=sr.Recognizer()
with sr.Microphone() as source:

    #read the audio data feom the default microphone

    audio_data=r.record(source,duration=5)
    print("Recognizing...")
    #convert speech to text
    text=r.recognize_google(audio_data)
    
    #text=r.recognize_google(audio_data,language="es-Es")
    print(text)

    if text=="open Google":   
       webbrowser.open('http://google.co.in', new=0, autoraise=True)
    elif text=="open YouTube":   
       webbrowser.open('http://youtube.co.in', new=0, autoraise=True)
    elif text=="open Wiki":   
       webbrowser.open('http://wikipedia.com', new=0, autoraise=True)
    elif text=="open Facebook":   
       webbrowser.open('http://facebook.com', new=0, autoraise=True)
    else:
        print("Sorry!!!This site is not available in our list..")
    