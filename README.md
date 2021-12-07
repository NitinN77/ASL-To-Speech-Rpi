# ASL-To-Speech-Rpi

A pi setup to recognize ASL signs using a pre-trained CNN model and speak it out using a suitable TTS engine with adaptive settings.

### Usage

```
1. git clone https://github.com/VoidlessVoid7/ASL-To-Speech-Rpi
2. cd ASL-To-Speech-Rpi
2. pip install -r requirements.txt
3. ./SoundWireServer
4. python3 sign_detector.py
```

### Working
1. sign_detector.py opens the primary camera and creates a region of interest for the detection
2. When movement is detected within the ROI, the background is separated using contour detection and blurring.
3. Hand signs are then recognized using the loaded keras CNN model which takes in the image matrix as input and provides a label(0-25) as output which is then mapped to the respective alphabet.
4. Recognized alphabets are added to a global buffer for processing.
5. When the user has finished input, the stop sign can be shown to end the infinite loop.
6. Once the loop breaks, all letters are mapped to their counts in a dictionary
7. The top N values are extracted with their original starting indices in the buffer and added to create the final word (the logic to handle duplicates is still in development) 
8. The tts is then called on the extracted word with settings based on the user’s internet connectivity status and location.  
