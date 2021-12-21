from pydub.playback import play
from pydub import AudioSegment


def run_voice():
    sound=AudioSegment.from_wav("C:/Users/Abhishek/Desktop/MINI_PROJECT_CONVOECOM/convoecom/tap1.mp3")
    play(sound)
    sound=AudioSegment.from_wav("C:/Users/Abhishek/Desktop/MINI_PROJECT_CONVOECOM/convoecom/tap2.mp3")
    play(sound)
    sound=AudioSegment.from_wav("C:/Users/Abhishek/Desktop/MINI_PROJECT_CONVOECOM/convoecom/tap3.mp3")
    play(sound)
    