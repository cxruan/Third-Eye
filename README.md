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
The prototype utilizes the Google Text-to-Speech python library to generate the sound reponse.

### Speech Recognition

### Sytereophonic Sound Rendering

## Challenges we ran into

## Accomplishments that we're proud of

## What we learned

## What's next for Third Eye
