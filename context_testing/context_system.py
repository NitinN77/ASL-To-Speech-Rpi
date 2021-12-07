import pandas as pd
import random


df = pd.read_csv('./dataset.csv')

user_prev_state = False

class Context():
    Camera_Module = None
    Nationality = None
    Gender = None
    Age = None
    User_Lang = None
    Camera_Flash = None
    Model = None
    Brightness = None
    tts_engine = None
    gps_module = None
    Amazon_API = None
    Latitude = None
    Longitude = None

    # PURELY DERIVED CONTEXT
    tts = None
    tts_status = None
    amplification = None
    pace = None
    voice = None

    def __init__(self, context):
        self.Camera_Module = context['Camera_Module']
        self.Nationality = context['Nationality']
        self.Gender = context['Gender']
        self.Age = context['Age']
        self.User_Lang = context['User_Lang']
        self.Camera_Flash = context['Camera_Flash']
        self.Model = context['Model']
        self.Brightness = context['Brightness']
        self.tts_engine = context['TTS_Engine']
        self.gps_module = context['GPS_Module']
        self.Amazon_API = context['Amazon_API']
        self.Latitude = context['Latitude']
        self.Longitude = context['Longitude']

    def getTTS(self):
        if self.Amazon_API:
            self.tts = 'Polly'
        else:
            # Hardware/Software Failure: Network Connection Unavailable / Cannot connect to the cloud
            self.tts = 'eSpeak'
        if self.tts_engine == 'Waiting for Input':
            self.tts_status = 'Ready'
        else:
            self.tts_status = 'Busy'
        

    def getTTSSettings(self):
        if self.User_Lang != 'None':
            # Manually fed Context
            if self.User_Lang == 'English':
                self.voice = 'en-US'
            elif self.User_Lang == 'Spanish':
                self.voice = 'es-US'
            elif self.User_Lang == 'French':
                self.voice = 'fr-FR'
            elif self.User_Lang == 'Italian':
                self.voice = 'it-IT'
            elif self.User_Lang == 'Chinese':
                self.voice = 'zh-CN'
            elif self.User_Lang == 'Japanese':
                self.voice = 'ja-JP'
            elif self.User_Lang == 'Hindi':
                self.voice = 'hi-IN'
            else:
                # Dead Context Fault: Unsupported Language, Defaulting to English
                self.voice = 'en-US'
        else:
            # Automatically derived Context using machine learning
            predicted_voice = 'en-US'
            if self.Nationality == 'English' or self.Nationality == 'American':
                predicted_voice = 'en-US'
            elif self.Nationality == 'Chinese':
                predicted_voice = 'zh-CN'
            elif self.Nationality == 'Japanese':
                predicted_voice = 'ja-JP'
            elif self.Nationality == 'Indian':
                predicted_voice = 'hi-IN'
            elif self.Nationality == 'Italian':
                predicted_voice = 'it-IT'
            elif self.Nationality == 'Spanish':
                predicted_voice = 'es-US'
            elif self.Nationality == 'French':
                predicted_voice = 'fr-FR'
            
            # confidence for nationality prediction
            nationality_confidence = random.choices(
                [0, 1], weights=(20, 80), k=1)[0]
            
            if nationality_confidence == 1 and predicted_voice:
                self.voice = predicted_voice

            location = None

            if self.gps_module:
                if self.Latitude > 18 and self.Latitude < 52 and self.Longitude > 76 and self.Longitude < 134:
                    location = 'zh-CN'
                elif self.Latitude > -10 and self.Latitude < -5 and self.Longitude > -75 and self.Longitude < -70:
                    location = 'ja-JP'
                elif self.Latitude > 6 and self.Latitude < 35 and self.Longitude > 67 and self.Longitude < 97:
                    location = 'hi-IN'
                elif self.Latitude > 90 or self.Latitude < -90 or self.Longitude > 180 or self.Longitude < -180:
                    # Dead Decision Fault i.e. (GPS functioning BUT values incorrect): Defaulting to en-US
                    location = 'en-US'
                else:
                    location = 'en-US'
                

            if nationality_confidence and self.gps_module:
                if location != self.voice:
                    # Conflicting Rules
                    # derived voice takes preference 
                    pass
            elif nationality_confidence == 0 and self.gps_module:
                # Fallback behaviour
                self.voice = location
            else:
                self.voice = predicted_voice
                # assume the best prediction for nationality even if not confident enough as a final case scenario
            


        if self.Age < 25:
            self.pace = 'fast'
            self.amplification = 'off'
        elif self.Age < 35:
            self.pace = 'medium'
            self.amplification = 'medium'
        else:
            self.pace = 'slow'
            self.amplification = 'high'



    def getFlash(self):
        if self.Brightness > 70:
            self.Camera_Flash = 'off'
        else:
            self.Camera_Flash = 'on'


    def check_context(self):
        global user_prev_state
        if self.Camera_Module == 'User Present':
            user_prev_state = True
            if self.Model == 0:
                # Software Failure
                print('Could not connect to model, Aborting. \n')
            else:
                print('Model connected')
                self.getTTS()
                self.getTTSSettings()
                self.getFlash()
                print('TTS Engine: ', self.tts)
                print('TTS Status: ', self.tts_status)
                print('Voice: ', self.voice)
                print('Amplification: ', self.amplification)
                print('Pace: ', self.pace)
                print('Flash: ', self.Camera_Flash)
                print('\n')

        elif self.Camera_Module == 'User Absent': 
            if user_prev_state == True:
                # Adaptation cycle fault: user was previously present, forcing a check
                print('User Absent, but user was previously present, forcing a check \n')
                if self.Model == 0:
                    # Software Failure
                    print('Could not connect to model, Aborting. \n')
                else:
                    print('Model connected')
                    self.getTTS()
                    self.getTTSSettings()
                    self.getFlash()
                    print('TTS Engine: ', self.tts)
                    print('TTS Status: ', self.tts_status)
                    print('Voice: ', self.voice)
                    print('Amplification: ', self.amplification)
                    print('Pace: ', self.pace)
                    print('Flash: ', self.Camera_Flash)
                    print('\n')
            else:
                print('User not detected. \n\n')
        else:
            # Hardware Failure
            print('Camera Module Error. \n\n')

for i, context in df.iterrows():
    c = Context(context)
    d = {df.columns[i]: context.values[i] for i in range(len(context.values))}
    print(d)
    print('\n')
    c.check_context()
    

        
