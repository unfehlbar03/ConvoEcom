import speech_recognition as speech
from pydub.playback import play
from pydub import AudioSegment
import pyttsx3
import threading

mic = speech.Microphone()
recog = speech.Recognizer()
msg=""
botVoiceEngine=pyttsx3.init()
botVoiceEngine.setProperty('rate', 125)     # setting up new voice rate
voices = botVoiceEngine.getProperty('voices')       # setting up the voice
botVoiceEngine.setProperty('voice', voices[0].id)

def play_bot(data_field):
    language = 'en'
    mytext="Please Tell Your "+data_field+" again"
    botVoiceEngine.save_to_file(mytext,"checkout.wav")
    botVoiceEngine.runAndWait()
    sound=AudioSegment.from_wav("checkout.wav")
    play(sound)
    

def mic_input(data_field):
    global msg
    t=5
    if data_field=="Address" :
            t=10
    if data_field=="Pin Code" or data_field=="Mobile Number" :
            t=7    
    with mic as source: 
        audio = recog.listen(source,phrase_time_limit=5)
        print("heard")
    try:
        msg=recog.recognize_google(audio)
        return msg
    except speech.UnknownValueError:
        return run_voice(data_field)    



def run_voice(data_field):
    t1=threading.Thread(target=play_bot,args=(data_field,))
    t2=threading.Thread(target=mic_input,args=(data_field,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    
    return msg