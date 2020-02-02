# Third Eye
HackSC-2020

## Inspiration
Third eye, AKA the Mind’s Eye or the Inner Eye, is a mystic concept originated from the Dharmic, Taoist, and Christian spiritual tradition. It is said that through spiritual training, even the blinds may obtain vision, or more than vision—a vision through space and time.

The latter part is undoubtedly beyond our knowledge, but we may be able to help the blind regain their vision.

## What it does
Our team integrates computer vision and text-to-speech into one device that can see the world for the blind people and mark it with the sound.

The device has two modes, scanning and searching. In the scanning mode, the Third Eye captures an image through the camera, and name everything it can tell with words. The generated sound signal is positioned in space such that the user can tell where the object is just by listening. In the searching mode, the device records the user’s voice after a beep. The word recorded determines what the device should look for. The searching result will be presented to the user stereophonically.

## How we built it

### Computer Vision
The app utilizes the AlwaysAI Computer Vision API to tags objects in the view of the webcam. AlwaysAI provides an easy-to-use program framework for a quick boot-start of development of a wide-range of computer vision software, great for Hackathons.
https://alwaysai.co/

We start from the real-time object detector starter-app provided by AlwaysAI and add the logic we needed on top of that. To improve the performance of the device, we changed the NN model to another pre-trained model found on AlwaysAI's website that uses a training set that can tag more kinds of objects.

### Text-to-speech
The prototype utilizes the Google Text-to-Speech python library to generate the response in '.mp3' format.
https://pypi.org/project/gTTS/

The '.mp3' files are then turned into '.wav' file using the pydub library.
https://pypi.org/project/pydub/

### Sytereophonic Sound Rendering
The generated speech is played with OpenAL via python binding library PyOpenAL.
https://pypi.org/project/PyOpenAL/
The position of the sound source is set based on the bounding box of the object.

### Speech Recognition
The keyword in search mode is captured with the python library provided by the Google Cloud Speech APL. The recording is sent to the cloud for speech recognition.
https://cloud.google.com/speech-to-text/

## Challenges we ran into

### Time Constraint
The time of the hackathon is limited so we have to take many options of expediency, they directly led to many of the other challenges we met.

### Unable to detect the accurate distance
The best solution of this device is to use 2 cameras and calculate the distance of objects via parallex effect. However, to make a quick prototype, we have to accomadate the pre-trained models we were provided.

### Lack of compiled OpenAL binaries
Unfortunately, OpenAL doesn't provide binaries for platforms other than Windows.

## Accomplishments that we're proud of
We made an app that works. The prototype meets the expectation and functions well.
We split the work evenly among teammates, and we focus on each team member's strength.

## What we learned
How to use the new APIs we found and time management skills.

## What's next for Third Eye
We want to first switch to a device with dual-cameras. We also want to train a new Neural Network model from scratch with the data collected or data sets available online.

More computation should be transferred to the cloud for better performance and less burden to the edge devices.

A localized version of language recognition logic would be provided as alternative so that object detection may be provided even when being unable to connect to the Internet.

A sonar may be added to the device as well, providing supplemental object detect support in dark environment.
