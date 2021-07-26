from pygame._sdl2 import get_num_audio_devices, get_audio_device_name #Get playback device names
from pygame import mixer #Playing sound
from pygame import event
import time
# mixer.init() #Initialize the mixer, this will allow the next command to work
# print([get_audio_device_name(x, 0).decode() for x in range(get_num_audio_devices(0))]) #Returns playback devices
# mixer.quit() #Quit the mixer as it's initialized on your main playback device

def streamAudio():

    mixer.init(devicename='VB-Cable') #Initialize it with the correct device

    mixer.music.load("outputAudio.mp3") #Load the mp3

    # audio = mixer.Sound("outputAudio.mp3")
    # audio_length = audio.get_length()
    mixer.music.play() #Play it
    
    # event.wait()
    time.sleep(5)

    mixer.music.stop()



# streamAudio()