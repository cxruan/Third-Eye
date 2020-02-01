from gtts import gTTS
import os
import time
from openal.audio import SoundSink, SoundSource
from openal.loaders import load_wav_file
from pydub import AudioSegment
import wave
import contextlib

temp_path = "C:\\Users\\YICHIY~1\\Documents\\Others\\HackSC\HackSC-2020\\realtime_object_detector\\temp_audio"


def make_sounds(items):

    sink = SoundSink()
    sink.activate()

    print([item.label for item in items])
    print([item.box.center for item in items])

    for item in items:
        label = item.label
        position = item.box.center
        area = item.box.area

        base_name = os.path.join(temp_path, label)
        wav_file = base_name + ".wav"

        if(not os.path.exists(wav_file)):

            tts = gTTS(label)
            tts.save(base_name + '.mp3')

            sound = AudioSegment.from_mp3(base_name + '.mp3')
            sound.export(wav_file, format="wav")

        data = load_wav_file(wav_file)

        duration = 0.0

        with contextlib.closing(wave.open(wav_file, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)

        source = SoundSource(position=[0, 0, 0])
        source.looping = False
        source.queue(data)

        sink.play(source)
        source.position = [0, 0, 0]
        sink.update()
        time.sleep(duration + 0.1)
