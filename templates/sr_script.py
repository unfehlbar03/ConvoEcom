import speech_recognition as speech
import websockets as web
import nltk
from nltk import tokenize
from operator import itemgetter
import math
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
import ast 
from playsound import playsound
import pyttsx3
from templates import speakBot
from pydub.playback import play
from pydub import AudioSegment
import threading
import time

nltk.download('punkt')        #EXECUTE THESE 2 LINES IN PYTHON FILE Seprately
nltk.download('stopwords')
botVoiceEngine=pyttsx3.init()
botVoiceEngine.setProperty('rate', 125)     # setting up new voice rate
voices = botVoiceEngine.getProperty('voices')       # setting up the voice
botVoiceEngine.setProperty('voice', voices[0].id)

language = 'en'
mytext="What would you like to search today?"
botVoiceEngine.save_to_file(mytext,"voice.wav")
botVoiceEngine.runAndWait()

mic = speech.Microphone()
recog = speech.Recognizer()
stopwords = set(stopwords.words('english'))
msg=""
def get_top_n(dict_elem, n):
    result = dict(sorted(dict_elem.items(), key = itemgetter(1), reverse = True)[:n]) 
    return result
def check_sent(word, sentences): 
    final = [all([w in x for w in word]) for x in sentences] 
    sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
    return int(len(sent_len))
mic = speech.Microphone()
recog = speech.Recognizer()
def play_bot():
    sound=AudioSegment.from_wav("../convoecom/voice.wav")
    play(sound)
    return
def mic_input():
    global msg
    with mic as source:
        print("Speak what you would like to search")
        audio = recog.listen(source,phrase_time_limit=6)
        print("Converting Speech to Text...")
        
    try:
       msg=recog.recognize_google(audio)
    except speech.UnknownValueError:
       msg=speakBot.run_voice()
    return(msg) 

    

def run_voice():
   
    t1=threading.Thread(target=play_bot)
    t2=threading.Thread(target=mic_input)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    
   #playsound("C:/Users/Abhishek/Desktop/MINI_PROJECT_CONVOECOM/convoecom/voice.mp3")
    doc =msg
    print(doc)
    total_words = doc.split()
    total_word_length = len(total_words)
    print(total_word_length)

    total_sentences = tokenize.sent_tokenize(doc)
    total_sent_len = len(total_sentences)
    print(total_sent_len)

    tf_score = {}
    for each_word in total_words:
        each_word = each_word.replace('.','')
        if each_word not in stopwords:
            if each_word in tf_score:
                tf_score[each_word] += 1
            else:
                tf_score[each_word] = 1

    # Dividing by total_word_length for each dictionary element
    tf_score.update((x, y/int(total_word_length)) for x, y in tf_score.items())


    idf_score = {}
    for each_word in total_words:
        each_word = each_word.replace('.','')
        if each_word not in stopwords:
            if each_word in idf_score:
                idf_score[each_word] = check_sent(each_word, total_sentences)
            else:
                idf_score[each_word] = 1

    # Performing a log and divide
    idf_score.update((x, math.log(int(total_sent_len)/y)) for x, y in idf_score.items())

    tf_idf_score = {key: tf_score[key] * idf_score.get(key, 0) for key in tf_score.keys()}


    #print(get_top_n(tf_idf_score, 5))
    Dict = get_top_n(tf_idf_score, 5)

    Dict2 = {
    "i":00,
    "me":00,
    "my":00,
    "please": 00,
    "find":00,
    "search":00,
    "color":00,
    "colour":00,
    "want":00,
    "need":00,
    }

    s = str(Dict).lower()
    Dict=ast.literal_eval(s)

    s = str(Dict2).lower()
    Dict2=ast.literal_eval(s)

    lis=[k for k in Dict if not k in Dict2]
    query=' '.join(map(str,lis))
    print(query)
    return query


