import time
import edgeiq
import cv2
from tts import make_sounds
import os
from multiprocessing import Process, Queue
import cv2
from voice_recognition import voice_recognition
from pydub.playback import play
from pydub import AudioSegment

"""
Use object detection to detect objects in the frame in realtime. The
types of objects detected can be changed by selecting different models.

To change the computer vision model, follow this guide:
https://dashboard.alwaysai.co/docs/application_development/changing_the_model.html

To change the engine and accelerator, follow this guide:
https://dashboard.alwaysai.co/docs/application_development/changing_the_engine_and_accelerator.html
"""

os.environ["PYAL_DLL_PATH"] = "C:\\Users\\YICHIY~1\\Documents\\Others\\HackSC"
empty_image_path = "C:\\Users\\Yichi Yang\\Documents\\Others\\HackSC\\HackSC-2020\\empty.png"
help_path = "C:\\Users\\YICHIY~1\\Documents\\Others\\HackSC\HackSC-2020\\audio\\help.mp3"

help_audio = AudioSegment.from_mp3(help_path) - 20


def make_sound_worker(q):
    while True:
        data = q.get()
        if data is None:
            break
        make_sounds(data)


def find_things_worker(q, labels):
    while True:
        data = q.get()
        if data is None:
            break
        word = voice_recognition(labels)
        items = [item for item in data if item.label.strip() == word]
        make_sounds(items, True)


def play_audio_worker(q):
    while True:
        data = q.get()
        if data is None:
            break
        play(data)


def main():

    obj_detect = edgeiq.ObjectDetection(
        "alwaysai/ssd_mobilenet_v2_coco_2018_03_29")
    obj_detect.load(engine=edgeiq.Engine.DNN)

    print("Loaded model:\n{}\n".format(obj_detect.model_id))
    print("Engine: {}".format(obj_detect.engine))
    print("Accelerator: {}\n".format(obj_detect.accelerator))
    print("Labels:\n{}\n".format(obj_detect.labels))

    fps = edgeiq.FPS()

    read_q = Queue()
    find_q = Queue()
    audio_q = Queue()

    captured_frame = cv2.imread(empty_image_path, cv2.IMREAD_COLOR)
    text = 'No objects yet...'

    try:
        with edgeiq.WebcamVideoStream(cam=0) as video_stream:
            # Allow Webcam to warm up
            time.sleep(2.0)

            read_worker = Process(target=make_sound_worker, args=(read_q,))
            read_worker.start()

            find_worker = Process(target=find_things_worker,
                                  args=(find_q, obj_detect.labels))
            find_worker.start()

            play_worker = Process(target=play_audio_worker,
                                  args=(audio_q,))
            play_worker.start()

            time.sleep(2.0)

            fps.start()

            # loop detection
            while True:

                frame = video_stream.read()
                results = obj_detect.detect_objects(frame, confidence_level=.5)
                frame = edgeiq.markup_image(
                    frame, results.predictions, colors=obj_detect.colors)

                key = cv2.waitKey(1) & 0xFF
                triggered = False
                if key == ord('q'):
                    break
                elif key == ord('s'):
                    captured_frame = frame

                    items = results.predictions
                    long_text = ", ".join([item.label.strip()
                                           for item in items])
                    if not long_text:
                        text = "Nothing Found"
                    elif len(long_text) <= 70:
                        text = long_text
                    else:
                        text = long_text[:70] + "..."

                    read_q.put(items)

                elif key == ord('f'):
                    captured_frame = frame

                    items = results.predictions
                    long_text = ", ".join([item.label.strip()
                                           for item in items])
                    if not long_text:
                        text = "Nothing Found"
                    elif len(long_text) <= 70:
                        text = long_text
                    else:
                        text = long_text[:70] + "..."

                    find_q.put(items)
                elif key == ord('h'):
                    audio_q.put(help_audio)
                    text = "Reading instructions..."

                panel = cv2.hconcat([frame, captured_frame])

                panel = cv2.copyMakeBorder(
                    panel, 10, 100, 10, 10, cv2.BORDER_CONSTANT, value=[255, 255, 255])
                panel = cv2.putText(panel, text, (10, 550),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
                panel = cv2.putText(panel, "Real Time", (22, 36),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA)
                panel = cv2.putText(panel, "Real Time", (20, 35),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
                panel = cv2.putText(panel, "Captured", (672, 36),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA)
                panel = cv2.putText(panel, "Captured", (670, 35),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.imshow('Third Eye Demo', panel)

                fps.update()

    finally:
        fps.stop()
        read_q.put(None)
        find_q.put(None)
        audio_q.put(None)

        print("elapsed time: {:.2f}".format(fps.get_elapsed_seconds()))
        print("approx. FPS: {:.2f}".format(fps.compute_fps()))

        print("Program Ending")


if __name__ == "__main__":
    main()
