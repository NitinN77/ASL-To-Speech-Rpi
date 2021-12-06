from polly import Polly
import sys
import geocoder
from geopy.geocoders import Nominatim
import subprocess
import socket


def is_connected():
    try:
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        pass
    return False


g = geocoder.ip('me')
geolocator = Nominatim(user_agent="geoapiExercises")
  

Latitude = str(g.latlng[0])
Longitude = str(g.latlng[1])
location = geolocator.reverse(Latitude+","+Longitude)
address = location.raw['address']
country = address.get('country', '')
voice = None

if country == 'India':
	voice = 'Aditi'
elif country == 'Italy':
	voice = 'Carla'
elif country == 'Japan':
	voice = 'Mizuki'
elif country == 'France':
	voice = 'Celine'

elif country == 'Spain':
	voice = 'Conchita'
elif country == 'United States of America':
	voice = 'Joanna'

connection = is_connected()

args = sys.argv
if connection:
	print('Connected to the internet')
	
	if len(args) == 3:
		voice = args[2]
		print('Forcing accent')
	else:
		print('Detected Country: ' + country)
	tts = Polly(voice)
	tts.say(args[1])
else:
	print('Internet connection unavailable')
	subprocess.call(["espeak", '"' + str(args[1]) + '"'])
	



