import RPi.GPIO as GPIO
import picamera, datetime
import os, os.path, sys, json, time
from quadlib import updater
from quadlib import convert
import thread

root = os.path.dirname(__file__) + '/'

camera = picamera.PiCamera()
camera.hflip = True
camera.vflip = True

with open(root+'config/settings.json') as sshsettingsfile:
	settings = json.load(sshsettingsfile)

isBoss = os.path.isfile(root+'percamconfig/boss')

if (not isBoss):
	with open(root+'percamconfig/bossip', 'r') as myfile:
		bossip = myfile.read().strip('\n')	
else:
	employees = updater.push(settings)

with open(root+'percamconfig/camerano', 'r') as camnofile:
	camerano = camnofile.read().strip('\n')
print "[root] Camera number(change it in camerano file): " + str(camerano)

if (isBoss):
	port = settings['gpioBossTriggerPort']
else:
	port = settings['gpioEmployeeTriggerPort']

GPIO.setmode(GPIO.BCM)
GPIO.setup(port, GPIO.IN, pull_up_down = GPIO.PUD_UP)


CAMLED = 32

# Set GPIO to output
GPIO.setup(CAMLED, GPIO.OUT, initial=False) 

# Five iterations with half a second
# between on and off
for i in range(3):
	GPIO.output(CAMLED,True) # On
	time.sleep(0.5)
	GPIO.output(CAMLED,False) # Off
	time.sleep(0.5)
GPIO.output(CAMLED,True) # Off
time.sleep(1.5)
GPIO.output(CAMLED,False)

if isBoss:
	triggerport = settings['gpioEmployeeTriggerPort']
	GPIO.setup( triggerport , GPIO.OUT )
	GPIO.output( triggerport, False )
	for i in employees:
		GPIO.setup( employees[i]['gpio'] , GPIO.OUT )
	        GPIO.output( triggerport, False )		

def takePicture(fileid):

        filename = settings['uploadpath']+fileid+'_'+str(camerano)+'_img.jpg'	

        print("[listener] Taking picture: " + filename)
	GPIO.output(CAMLED,True)
        camera.capture(filename)
	GPIO.output(CAMLED,False)

	return filename;

def generateFileId():
	return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def loadCameraSettings():
        with open(root + 'config/camerasettings.json') as camsettingsfile:
                return json.load(camsettingsfile)

def saveCameraSettings(cameraSettings):
        with open(root + 'config/camerasettings.json', 'w') as outfile:
                json.dump(cameraSettings, outfile)

def loadCameraSettings():
        with open(root + 'config/camerasettings.json') as camsettingsfile:
                return json.load(camsettingsfile)

def saveCameraSettings(cameraSettings):
        with open(root + 'config/camerasettings.json', 'w') as outfile:
                json.dump(cameraSettings, outfile)

def triggerEmployees(val):
        for i in employees:
                GPIO.output( employees[i]['gpio'], val )

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
		triggerEmployees( True )
	else: 
		cameraSettings = loadCameraSettings()		
		fileid = cameraSettings['nextid']

	filename = takePicture(fileid)

	if GPIO.input(port):
		GPIO.wait_for_edge(port, GPIO.FALLING)
			
	if isBoss:
		triggerEmployees(False)
		print "[listener] i is the boss, creating gif..."

		thread.start_new_thread( convert.waitForFiles, (fileid, employees, settings, cameraSettings, ))		
#		thread = Thread( convert.waitForFiles, args = (fileid, employees, settings, cameraSettings))
#		thread.start()
#		convert.waitForFiles(fileid, employees, settings, cameraSettings);
	
	if not isBoss:
		print "[listener] i am an employee. Uploading image to boss@" + bossip		
		updater.uploadPhoto(filename, bossip, settings)

	print("[listener] Picture took. Listening.")

GPIO.cleanup()
