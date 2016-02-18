import RPi.GPIO as GPIO
import picamera, datetime
import os, os.path, sys, json
import updater


camera = picamera.PiCamera()
camera.hflip = True
camera.vflip = True


with open('sshsettings.json') as sshsettingsfile:
	sshsettings = json.load(sshsettingsfile)

isBoss = not os.path.isfile('bossip')

if (not isBoss):
	with open('bossip', 'r') as myfile:
		bossip = myfile.read()
else:
	updater.push(sshsettings)

sys.exit()


with open('camerano', 'r') as camnofile:
	camerano = camnofile.read()
print "Camera number(change it in camerano file): " + str(camerano)



folder = "camera"

port = 14

GPIO.setmode(GPIO.BCM)

GPIO.setup(port, GPIO.IN, pull_up_down = GPIO.PUD_UP)


def takePicture():
	tm = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        filename = folder+'/'+tm+'_'+str(camerano)+'_img.jpg'

        print("Taking picture: " + filename)

        camera.capture(filename)

	return filename;

def createGif(filename):
	
	print 'converting gif ' + filename

while True:

	GPIO.wait_for_edge(port, GPIO.RISING)

	filename = takePicture();

	if GPIO.input(port):
		GPIO.wait_for_edge(port, GPIO.FALLING)

	if isBoss:
		print "i is the boss"

		createGif
	
	if not isBoss:
		print "uploading image to " + bossip
		
		updater.uploadPhoto(filename, sshsettings)

	print("Done!")

GPIO.cleanup()
