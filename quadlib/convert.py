import time, os

def waitForFiles(id, settings):
	print "[convert] waiting for files of " + id
	#lol, good enough for the demo...
	time.sleep(5)
	createGif(id, settings)

def createGif(id, settings):	
	cmd = 'convert -delay 50  -size 400x300 '
	for i in range(1, settings['cameracount']):
		cmd += '-page '+ id + '_' + str(i) + '.jpg'
	cmd += 'loop 0 ' + id + '.gif'
	
	os.system(cmd)

