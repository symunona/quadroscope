
import picamera, datetime
import os, os.path, sys, json, time
from quadlib import updater.Updater, convert, gui

import thread
from quadlib import utils, utils.CameraWrapper, gpio.GPIO, camera_loop.camera_loop


root = os.path.dirname(__file__) + '/'

settings = json.load(open(root+'config/settings.json'))
boss = os.path.isfile(root+'percamconfig/boss')
camerano = open(root+'percamconfig/camerano', 'r').read().strip('\n')

updater = Updater(settings, camerano)

if (not boss):
	bossip = myfile.read().strip('\n')			
else:
	# employees = updater.push(settings)
    pass

print "[root] Camera number(change it in camerano file): " + str(camerano)

gpio = GPIO(settings, boss)
camera = utils.CameraWrapper.CameraWrapper(picamera)

# show user that we are starting
gpio.blinkCamera(4)

# start gui
thread.start_new_thread(gui.main, (camera,))
    
print "[listener] listening on port " + str(gpio.port)

# start camera loop
camera_loop( updater, gpio, camera )

