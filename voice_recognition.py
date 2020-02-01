import speech_recognition as sr

# labels of the pretrained data set
LABELS = ['person', 'bottle']

# obtain audio from the microphone
def voice_recognition():
    r = sr.Recognizer()
    with sr.Microphone(device_index=0) as source:
        print("Speak the object")
        audio = r.listen(source, phrase_time_limit=2)

    # recognize speech using Google Speech Recognition
    try:
        res = r.recognize_google(audio, show_all=True)
        print("Results from Google Speech Recognition API:")
        print(res)
        if res:
            words = map(lambda f: f['transcript'], res['alternative'] )
            for word in words:
                if word in LABELS:
                    print("Google Speech Recognition think you said: %s", word)
                    return word
            print("Google Speech Recognition results don't match data set labels")
        else:
            print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

if __name__ == "__main__":
    voice_recognition()


