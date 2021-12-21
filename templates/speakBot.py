import speech_recognition as speech
from pydub.playback import play
from pydub import AudioSegment
import threading
import pyttsx3

botVoiceEngine=pyttsx3.init()
botVoiceEngine.setProperty('rate', 125)     # setting up new voice rate
voices = botVoiceEngine.getProperty('voices')       # setting up the voice
botVoiceEngine.setProperty('voice', voices[0].id)

language = 'en'
mytext="Please Try To Search Again"
botVoiceEngine.save_to_file(mytext,"try.mp3")
botVoiceEngine.runAndWait()

mic = speech.Microphone()
recog = speech.Recognizer()
msg=""
def play_bot():
    sound=AudioSegment.from_wav("../convoecom/try.mp3")
    play(sound)

def mic_input():
    global msg
    with mic as source:
        audio = recog.listen(source, phrase_time_limit=6)
    try:
        msg=recog.recognize_google(audio)
        return msg
    except speech.UnknownValueError:
        return run_voice()    



def run_voice():
    t1=threading.Thread(target=play_bot)
    t2=threading.Thread(target=mic_input)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    
    return msg
   
   



