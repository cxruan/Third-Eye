import speech_recognition as sr
from pydub.playback import play
from pydub import AudioSegment

# labels of the pretrained data set
LABELS = ['person', 'bottle']

beep_path = "C:\\Users\\YICHIY~1\\Documents\\Others\\HackSC\HackSC-2020\\audio\\beep-06.wav"
beep = AudioSegment.from_wav(beep_path) - 24

# obtain audio from the microphone
def voice_recognition(labels):
    labels = [label.strip() for label in labels] if labels else LABELS

    r = sr.Recognizer()
    r.energy_threshold = 600
    with sr.Microphone(device_index=0) as source:
        print("Say something...")
        play(beep)
        audio = r.listen(source, phrase_time_limit=2)

    # recognize speech using Google Speech Recognition
    try:
        res = r.recognize_google(audio, show_all=True)
        print("Results from Google Speech Recognition API:")
        print(res)
        if res:
            words = map(lambda f: f['transcript'], res['alternative'])
            for word in words:
                if word in labels:
                    print("Google Speech Recognition think you said: %s" % word)
                    return word
            print("Google Speech Recognition results don't match data set labels")
        else:
            print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(e))
