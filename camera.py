
import picamera, datetime
import os, os.path, sys, json, time
from quadlib import updater.Updater, convert, gui

import thread
from quadlib import utils, utils.CameraWrapper, gpio.GPIO

root = os.path.dirname(__file__) + '/'

settings = json.load(open(root+'config/settings.json'))
boss = os.path.isfile(root+'percamconfig/boss')
camerano = open(root+'percamconfig/camerano', 'r').read().strip('\n')

updater = updater.Updater()

if (not boss):
	bossip = myfile.read().strip('\n')			
else:
	# employees = updater.push(settings)
    pass

print "[root] Camera number(change it in camerano file): " + str(camerano)

gpio = GPIO(settings, boss)
gpio.blinkCamera(4)

camera = utils.CameraWrapper.CameraWrapper(picamera)

thread.start_new_thread(gui.main, (camera,))
    
fileid = camera.generateFileId()
    
print "[listener] listening on port " + str(gpio.port)

while True:

	gpio.wait_for_trigger()

	# if boss, then upload settings to other cameras
	if isBoss:
        print "[listener] sending camera settings"        
		triggerEmployees( True )
	else: 
		# camera_settings = loadcamera_settings()		
		# fileid = camera_settings['nextid']

	filename = camera.take_picture(fileid)


	if GPIO.input(port):
		GPIO.wait_for_edge(port, GPIO.FALLING)
			
	if isBoss:
		triggerEmployees(False)
		print "[listener] i is the boss, creating gif..."

		thread.start_new_thread( convert.waitForFiles, (fileid, employees, settings, camera_settings, ))		

#		thread = Thread( convert.waitForFiles, args = (fileid, employees, settings, camera_settings))
#		thread.start()
#		convert.waitForFiles(fileid, employees, settings, camera_settings);
	
	if not isBoss:
		print "[listener] i am an employee. Uploading image to boss@" + bossip		
		updater.uploadPhoto(filename, bossip, settings)

	print("[listener] Picture took. Listening.")

GPIO.cleanup()
