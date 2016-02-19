import time, os

def waitForFiles(id, employees, settings):
	print "[convert] waiting for files of " + id
	#lol, good enough for the demo...
	time.sleep(5)
	createGif(id, employees, settings)

def createGif(id, employees, settings):	
	cmd = 'convert -delay 14 -size 640x480 -loop 0 '

	pictureCnt = len(employees.keys())
	for i in range(pictureCnt):
		filename = settings['uploadpath'] + id + '_' + str(i+1) + '_img.jpg'
		if os.path.exists(filename):
			cmd += filename +' '
        for i in range(pictureCnt-2):
                filename = settings['uploadpath'] + id + '_' + str(pictureCnt-i-1) + '_img.jpg'
                if os.path.exists(filename):
                        cmd += filename +' '

	cmd +=  settings['uploadpath'] + id + '640.gif'
	print '[convert] ' + cmd
	os.system(cmd)

