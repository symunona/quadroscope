import time, os

def waitForFiles(id, settings):
	print "[convert] waiting for files of " + id
	#lol, good enough for the demo...
	time.sleep(5)
	createGif(id, settings)

def createGif(id, settings):	
	cmd = 'convert -delay 50 -size 640x480 -loop 0 '
	for i in range(0, settings['cameracount']):
		cmd += settings['uploadpath'] + id + '_' + str(i+1) + '_img.jpg '
	cmd +=  settings['uploadpath'] + id + '640.gif'
	print '[convert] ' + cmd
	os.system(cmd)

