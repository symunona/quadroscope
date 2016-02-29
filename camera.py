import os, os.path, sys, json, time, thread, datetime
import picamera
 

from quadlib import convert, gui
from quadlib.updater import Updater
from quadlib.utils.gpio import Gpio
from quadlib import client
from quadlib.CameraWrapper import CameraWrapper

root = os.path.dirname(__file__) + '/'

print '[root] ', root
print '[__file__] ', __file__

settings = json.load(open(root+'config/settings.json'))
boss = os.path.isfile(root+'percamconfig/boss')
camerano = open(root+'percamconfig/camerano', 'r').read().strip('\n')
        
updater = Updater(settings, camerano, boss)

if (not boss):
	bossip = myfile.read().strip('\n')			
else:
	# employees = updater.push(settings)
    pass

print "[root] Camera number(change it in camerano file): " + str(camerano)

gpio = Gpio(settings, boss)

camera = CameraWrapper(picamera.PiCamera(), updater, gpio, boss, camerano)

# show user that we are starting
gpio.blinkCamera(4)
    
print "[listener] listening on port " + str(gpio.port)

# start camera loop
if boss:
    gui.main(settings, boss, updater, camera)
else:
    client.camera_loop( updater, gpio, camera )

