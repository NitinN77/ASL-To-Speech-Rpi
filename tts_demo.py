from polly import Polly

tts = Polly('Joanna')
tts.say('Sample text, hello there!')
tts.saveToFile('Hi there, save the speech for later', 'joanna.mp3')
