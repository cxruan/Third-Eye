# Third Eye
HackSC-2020

## Inspiration
Third eye, AKA the Mind’s Eye or the Inner Eye, is a mystic concept originated from the Dharmic, Taoist, and Christian spiritual tradition. It is said that through spiritual training, even the blinds may obtain vision, or more than vision—a vision through space and time.

The latter part is undoubtedly beyond our knowledge, but we may be able to help the blind regain their vision.

## What it does
Our team integrates computer vision and text-to-speech into one device that can see the world for the blind people and mark it with the sound.

The device has two modes, scanning and searching. In the scanning mode, the Third Eye will capture an image through the camera, and name everything it can tell with words. The generated sound signal will be modified stereophonically, such that the user will be able to recognize the position and distance of the item via sound. In the searching mode, the device will record the user’s voice after a beep sound. The word recorded will determine what the device should be looking for. The searching result will be replied to the user stereophonically.

## How we built it

### Computer Vision
The project prototype utilizes the Always AI Computer Vision API to build the Computer Vision module of the device. The Always AI provides an easy-to-use program framwork for a quick boot-start of development of a wide-range of computer vision software, great for Hackathons.
https://alwaysai.co/

We start from the realtime object detector starter-app provided and add the logic we needed on top of that. To improve the performance of the device, we changed the NN model used to another pre-trained model found on Always AI's website that utilizes a training set with more available tags.

### Text-to-speech
The prototype utilizes the Google Text-to-Speech python library to generate the sound reponse in '.mp3' version.
https://pypi.org/project/gTTS/

The '.mp3' file is then turned into '.wav' file via the pydub library for playing.
https://pypi.org/project/pydub/

### Sytereophonic Sound Rendering
The original sound is played with OpenAL via python binding library PyOpenAL.
https://pypi.org/project/PyOpenAL/
The volume is manipulated with the position fed by the computer vision module. The distance of the object is approximated with the inverse square root of the object box's area.

### Speech Recognition
The keyword in search mode is captured with the python library provided by the Google Cloud Speech APL. The recording is later transferred to the cloud for speech recognition.
https://cloud.google.com/speech-to-text/

## Challenges we ran into

### Time Constraint
The time of the hackathon is limited so we have to take many options of expediency, they directly led to many of the other challenges we met.

### Unable to detect the accurate distance
The best solution of this device is to use 2 cameras and calculate the distance of objects via parallex effect. However, to make a quick prototype, we have to accomadate the pre-trained models we were provided.

### Lack of compiled OpenAL binaries
Unfortunately, OpenAL doesn't provide binaries for platforms other than Windows.

## Accomplishments that we're proud of
We have a clear distribution of work that focuses on each team member's strength.

## What we learned
How t use the new APIs w found and time management skills.

## What's next for Third Eye
We would first switch to a device with dual-camera. A new Neural Network will be trained from scratch with the data collected or hopefully with new training sets found online.

More computation should be transferred to the cloud for better performance and less burden to the edge devices.

A localized version of language recognition logic would be provided as alternative so that object detection may be provided even when being unable to connect to the Internet.

A sonar may be added to the device as well, providing supplemental object detect support in dark environment.
