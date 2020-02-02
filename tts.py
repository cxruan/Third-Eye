from gtts import gTTS
import os
import time
from openal.audio import SoundSink, SoundSource
from openal.loaders import load_wav_file
from pydub import AudioSegment
import wave
import contextlib
import math
from pydub.playback import play
from pydub import AudioSegment

temp_path = "C:\\Users\\YICHIY~1\\Documents\\Others\\HackSC\HackSC-2020\\temp_audio"
audio_path = "C:\\Users\\YICHIY~1\\Documents\\Others\\HackSC\HackSC-2020\\audio"

not_found = AudioSegment.from_mp3(os.path.join(audio_path, "404.mp3")) - 20

frame_width = 640
frame_height = 480
frame_area = frame_width * frame_height

# tts = gTTS("This app helps blind people see the world. Press S key to use scan mode. In scan mode,"
# + " the app reads everything out loud it finds in its view. The direction of the sound corresponds to the "
# + "position of the object in real world. Press F key to use find mode. In find mode, You name the thing you "
# + "want to find after the beep, and the app will only look for that object. Press h key to listen to "
# + "this instruction again.")
# tts.save(os.path.join(temp_path, "help") + '.mp3')

# tts = gTTS("is in front of you")
# tts.save(os.path.join(temp_path, "front") + '.mp3')
# sound = AudioSegment.from_mp3(os.path.join(temp_path, "front") + '.mp3')
# sound.export(os.path.join(temp_path, "front.wav"), format="wav")

left = load_wav_file(os.path.join(audio_path, "left.wav"))
slight_left = load_wav_file(os.path.join(audio_path, "slight_left.wav"))
front = load_wav_file(os.path.join(audio_path, "front.wav"))
slight_right = load_wav_file(os.path.join(audio_path, "slight_right.wav"))
right = load_wav_file(os.path.join(audio_path, "right.wav"))


def get_duration(file):
    with contextlib.closing(wave.open(file, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        return frames / float(rate)


left_duration = get_duration(os.path.join(audio_path, "left.wav"))
slight_left_duration = get_duration(
    os.path.join(audio_path, "slight_left.wav"))
front_duration = get_duration(os.path.join(audio_path, "front.wav"))
slight_right_duration = get_duration(
    os.path.join(audio_path, "slight_right.wav"))
right_duration = get_duration(os.path.join(audio_path, "right.wav"))


def make_sounds(items, verbose=False):

    sink = SoundSink()
    sink.activate()

    print("Frame with these items: " + str([item.label for item in items]))

    if not items:
        play(not_found)

    for item in items:
        label = item.label.strip()
        position = item.box.center
        area = item.box.area

        source_x = (position[0] - frame_width / 2) / (frame_width / 2) * 5
        source_z = -1 / math.sqrt(area / frame_area) * 1.5

        print("{label} @ ({x:2f}, {z:2f})".format(
            label=label, x=source_x, z=source_z))

        base_name = os.path.join(temp_path, label)
        wav_file = base_name + ".wav"

        if(not os.path.exists(wav_file)):

            tts = gTTS(label)
            tts.save(base_name + '.mp3')

            sound = AudioSegment.from_mp3(base_name + '.mp3')
            sound.export(wav_file, format="wav")

        data = load_wav_file(wav_file)

        duration = get_duration(wav_file)

        source = SoundSource(position=[0, 0, 0])
        source.looping = False
        source.queue(data)

        if verbose:
            prompt = None
            prompt_duration = 0.0
            if source_x < -2.5:
                prompt = left
                prompt_duration = left_duration
            elif source_x < -1:
                prompt = slight_left
                prompt_duration = slight_left_duration
            elif source_x < 1:
                prompt = front
                prompt_duration = front_duration
            elif source_x < 2.5:
                prompt = slight_right
                prompt_duration = slight_right_duration
            else:
                prompt = right
                prompt_duration = right_duration

            source.queue(prompt)
            duration += prompt_duration

        sink.play(source)
        source.position = [source_x, 0, source_z]
        sink.update()
        time.sleep(duration + 0.1)
