import RPi.GPIO as GPIO
import picamera, datetime
import os, os.path, sys, json
from quadlib import updater
from quadlib import convert

root = os.path.dirname(__file__) + '/'
#print "project root " +root + " file: " + __file__
camera = picamera.PiCamera()
camera.hflip = True
camera.vflip = True

with open(root+'config/settings.json') as sshsettingsfile:
	settings = json.load(sshsettingsfile)

isBoss = not os.path.isfile(root+'percamconfig/bossip')

if (not isBoss):
	with open(root+'percamconfig/bossip', 'r') as myfile:
		bossip = myfile.read().strip('\n')
	
#	print '[root] i am an employee. The boss is ' + bossip
else:
	employees = updater.push(settings)
#	print '[root] i am the boss ' + root+'percamconfig/bossip'

#sys.exit()

with open(root+'percamconfig/camerano', 'r') as camnofile:
	camerano = camnofile.read().strip('\n')
print "[root] Camera number(change it in camerano file): " + str(camerano)



def loadCameraSettings():
	with open(root + 'config/camerasettings.json') as camsettingsfile:
        	return json.load(camsettingsfile)

def saveCameraSettings(cameraSettings):
        with open(root + 'config/camerasettings.json', 'w') as outfile:
                json.dump(cameraSettings, outfile)


if (isBoss):
	port = settings['gpioBossTriggerPort']
else:
	port = settings['gpioEmployeeTriggerPort']

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(port, GPIO.IN, pull_up_down = GPIO.PUD_UP)

if isBoss:
	triggerport = settings['gpioEmployeeTriggerPort']
	GPIO.setup( triggerport , GPIO.OUT )
	GPIO.output( triggerport, False )

def takePicture(fileid):

        filename = settings['uploadpath']+'/'+fileid+'_'+str(camerano)+'_img.jpg'	

        print("[listener] Taking picture: " + filename)

        camera.capture(filename)

	return filename;

def generateFileId():
	return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def loadCameraSettings():
        with open(root + 'config/camerasettings.json') as camsettingsfile:
                return json.load(camsettingsfile)

def saveCameraSettings(cameraSettings):
        with open(root + 'config/camerasettings.json', 'w') as outfile:
                json.dump(cameraSettings, outfile)


cameraSettings = loadCameraSettings()
	
print "[listener] listening on port " + str(port)
while True:

	GPIO.wait_for_edge(port, GPIO.RISING)

	fileid = generateFileId()  
	# if boss, then upload settings to other cameras
	if isBoss:
                print "[listener] sending camera settings"
		cameraSettings['nextid'] = fileid
		saveCameraSettings(cameraSettings)
		updater.syncCameraSettings(employees, settings)	
		GPIO.output(triggerport, True)
	else: 
		cameraSettings = loadCameraSettings()		
		fileid = cameraSettings['nextid']

	filename = takePicture(fileid)

	if GPIO.input(port):
		GPIO.wait_for_edge(port, GPIO.FALLING)
			
	if isBoss:
		GPIO.output(triggerport, False)
		print "[listener] i is the boss, creating gif..."
		convert.waitForFiles(fileid, settings);
	
	if not isBoss:
		print "[listener] i am an employee. Uploading image to boss@" + bossip		
		updater.uploadPhoto(filename, bossip, settings)

	print("[listener] Picture took. Listening.")

GPIO.cleanup()
