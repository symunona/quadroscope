#
#   Quadroscope - entry point
#
#   The four camera system for raspberries.
#   

import os, os.path, sys, json, time, thread, datetime
import picamera
 
from quadlib.utils import log
from quadlib import convert
from quadlib.updater import Updater
from quadlib.utils.gpio import Gpio
from quadlib import client
from quadlib.CameraWrapper import CameraWrapper

root = os.path.dirname(__file__) + '/'
log('[startup] ----------------------------------------', time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.localtime()))
log('[root] ', root)
log('[__file__] ', __file__)

# Read the settings from the `config` and `percamconfig` folders.
# settings.json stores generic data:
#   - credentials for the other pi's (should be the same for every pi)
#   - upload path: this is where the employees will upload the pictures made
#   - ssh path: this is where the boss will copy the most recent code files.
# GPIO:
#   triggering ports for writing settings and making a picture
#   - gpioBossTriggerPort: the GPIO pin on which the trigger is set
#   - gpioHigh: once done with uploading settings, boss triggers this port to let the others know to make a pic
#   - gpioEmployeeTriggerPort: if this is an employee, it will listen on this port for the shooting trigger

settings = json.load(open(root+'config/settings.json'))

# If file exists, this is the boss.
boss = os.path.isfile(root+'percamconfig/boss')

# If for some reason one of the cameras are flipped, set these files.
vflip = os.path.isfile(root+'percamconfig/vflip')
hflip = os.path.isfile(root+'percamconfig/hflip')

# The camera number.
camerano = open(root+'percamconfig/camerano', 'r').read().strip('\n')
        
debug = False
push = True

# FLAGS:
#   -- debug: I have no clue what it does.
for arg in sys.argv: 
    if arg == '--debug': debug = True
    if arg == '--restartall':
        updater = Updater(camerano, boss, False)
        updater.restart_employees()
        sys.exit()
    if arg == '--update':
        updater = Updater(camerano, boss, True)                
        sys.exit()
    if arg == '--status':
        updater = Updater(camerano, boss, True)                
        updater.status()
        sys.exit()
    if arg == '--nopush':
        push = False
        
updater = Updater(camerano, boss, debug)
if boss:
    updater.push()

log("[root] Camera number(change it in camerano file): " + str(camerano))

gpio = Gpio(settings, boss)

picam_object = picamera.PiCamera()
picam_object.hflip = False

picam_object.vflip = vflip
picam_object.hflip = hflip

camera = CameraWrapper(picam_object, updater, gpio, boss, camerano)

# show user that we are starting
gpio.blinkCamera(4)
    
log( "[listener] listening on port " + str(gpio.port))

# start camera loop
if boss:
    from quadlib import gui 
    gui.main(settings, boss, updater, camera)
    # Restart all the other cameras by default.
    updater = Updater(camerano, boss, False)
    updater.restart_employees()
else:
    updater.pull()
    client.camera_loop( updater, gpio, camera )

