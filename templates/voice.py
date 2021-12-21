import speech_recognition as speech
import pyttsx3
from gtts import gTTS
from pydub.playback import play
from pydub import AudioSegment  
import time
from playsound import playsound
import asyncio
import threading
from templates import checkout_info

botVoiceEngine=pyttsx3.init()
botVoiceEngine.setProperty('rate', 125)     # setting up new voice rate
voices = botVoiceEngine.getProperty('voices')       # setting up the voice
botVoiceEngine.setProperty('voice', voices[0].id)

mic = speech.Microphone()
recog = speech.Recognizer()
msg=""

def run_voice(data_field):
    language = 'en'
    mytext="Please Tell Your "+data_field
    botVoiceEngine.save_to_file(mytext,"checkout.wav")
    #myobj = gTTS(text=mytext, lang=language, slow=False)
    #myobj.save("voice.mp3")
    botVoiceEngine.runAndWait()
    sound=AudioSegment.from_wav("checkout.wav")
    play(sound)
    return

def mic_inp(data_field):
    global msg
    with mic as source:
        t=8
        if data_field=="Address" :
            t=10
        if data_field=="Pin Code":
            t=7    
        if data_field=="Mobile Number":
            t=10
        recog.adjust_for_ambient_noise(source)
        audio = recog.listen(source,phrase_time_limit=t)
    try:
       msg=recog.recognize_google(audio)
    except speech.UnknownValueError:
        msg =checkout_info.run_voice(data_field)  
    return msg
    
    

def data_to_enter(query):
   t1=threading.Thread(target=run_voice,args=(query,))
   t2=threading.Thread(target=mic_inp,args=(query,)) 
   t1.start()
   t2.start()
   t1.join()
   t2.join()
   return msg
       