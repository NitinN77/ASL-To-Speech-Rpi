import pandas as pd
import random
import time
random.seed(time.process_time())


Camera_Module = ['User Present'] * 9 + ['User Absent'] + ['Cannot connect to camera']
Nationality = ['Chinese', 'American', 'English', 'Indian', 'Japanese', 'French', 'Italian'] + ['None'] * 2
Gender = ['Male', 'Female']
Age = [random.randint(15, 50) for i in range(100)]
User_Lang = ['Hindi', 'English', 'Italian', 'French', 'Japanese', 'Chinese', 'Spanish'] + ['None'] * 2
Camera_Flash = [1, 0]
Model = [1] * 9 + [0]
Brightness = [random.uniform(0, 100) for i in range(100)]
TTS_Engine = ['Waiting for Input'] * 8 + ['Converting text to speech'] + ['Playing audio']
GPS_Module = [1] * 7 + [0] * 3
Amazon_API = [1] * 7 + [0] * 3

Latitude = [random.uniform(-90, 90) for i in range(100)]
Longitude = [random.uniform(-180, 180) for i in range(100)]

contexts = [Camera_Module, Nationality, Gender, Age, User_Lang, 
Camera_Flash, Model, Brightness, TTS_Engine, GPS_Module, Amazon_API, Latitude, Longitude]


df = pd.DataFrame(
    columns=['Camera_Module', 'Nationality', 'Gender', 'Age', 'User_Lang', 
'Camera_Flash', 'Model', 'Brightness', 'TTS_Engine', 'GPS_Module', 'Amazon_API', 'Latitude', 'Longitude'])

for i in range(100):
    r = []
    for context in contexts:
        r.append(random.choice(context))
    df.loc[len(df)] = r


print(df)
df.to_csv('./dataset.csv', index=False)
