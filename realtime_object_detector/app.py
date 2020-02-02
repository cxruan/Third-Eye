import time
import edgeiq
import cv2
from tts import make_sounds
import os
from multiprocessing import Process, Queue
import cv2

"""
Use object detection to detect objects in the frame in realtime. The
types of objects detected can be changed by selecting different models.

To change the computer vision model, follow this guide:
https://dashboard.alwaysai.co/docs/application_development/changing_the_model.html

To change the engine and accelerator, follow this guide:
https://dashboard.alwaysai.co/docs/application_development/changing_the_engine_and_accelerator.html
"""

os.environ["PYAL_DLL_PATH"] = "C:\\Users\\YICHIY~1\\Documents\\Others\\HackSC"
empty_image_path = "C:\\Users\\Yichi Yang\\Documents\\Others\\HackSC\\HackSC-2020\\realtime_object_detector\\empty.png"


def make_sound_worker(q):
    while True:
        data = q.get()
        if not data:
            break
        make_sounds(data)


def main():

    obj_detect = edgeiq.ObjectDetection(
        "alwaysai/mobilenet_ssd")
    obj_detect.load(engine=edgeiq.Engine.DNN)

    print("Loaded model:\n{}\n".format(obj_detect.model_id))
    print("Engine: {}".format(obj_detect.engine))
    print("Accelerator: {}\n".format(obj_detect.accelerator))
    print("Labels:\n{}\n".format(obj_detect.labels))

    fps = edgeiq.FPS()

    q = Queue()

    captured_frame = cv2.imread(empty_image_path, cv2.IMREAD_COLOR)
    text = 'No objects yet...'

    try:
        with edgeiq.WebcamVideoStream(cam=0) as video_stream:
            # Allow Webcam to warm up
            time.sleep(2.0)
            fps.start()

            worker = Process(target=make_sound_worker, args=(q,))
            worker.start()

            # loop detection
            while True:

                # if items:
                #     make_sounds(items)
                #     items = None

                frame = video_stream.read()
                results = obj_detect.detect_objects(frame, confidence_level=.5)
                frame = edgeiq.markup_image(
                    frame, results.predictions, colors=obj_detect.colors)

                key = cv2.waitKey(1) & 0xFF
                triggered = False
                if key == ord('q'):
                    break
                elif key == ord(' '):
                    captured_frame = frame

                    items = results.predictions
                    long_text = ", ".join([item.label for item in items])
                    text = long_text if len(long_text) <= 70 else long_text[:70] + "..."

                    q.put(items)

                panel = cv2.hconcat([frame, captured_frame])

                panel = cv2.copyMakeBorder(
                    panel, 10, 100, 10, 10, cv2.BORDER_CONSTANT, value=[255, 255, 255])
                panel = cv2.putText(panel, text, (10, 550),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
                cv2.imshow('Super Cool App', panel)

                fps.update()

    finally:
        fps.stop()
        q.put(None)
        print("elapsed time: {:.2f}".format(fps.get_elapsed_seconds()))
        print("approx. FPS: {:.2f}".format(fps.compute_fps()))

        print("Program Ending")


if __name__ == "__main__":
    main()
