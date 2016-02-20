import time, os

def waitForFiles(id, employees, settings, camerasettings):
	print "[convert] waiting for files of " + id
	#lol, good enough for the demo...
	time.sleep(6)
	createGif(id, employees, settings, camerasettings)

def createGif(id, employees, settings, camerasettings):	
	cmd = 'convert -delay '+str(camerasettings['delay'])+' -size 640x480 -loop 0 '
	foundpics = 0
	pictureCnt = len(employees.keys())
	for i in range(pictureCnt):
		filename = settings['uploadpath'] + id + '_' + str(i+1) + '_img.jpg'
		if os.path.exists(filename):
			foundpics += 1;
			cmd += filename +' '
        for i in range(pictureCnt-2):
                filename = settings['uploadpath'] + id + '_' + str(pictureCnt-i-1) + '_img.jpg'
                if os.path.exists(filename):
                        cmd += filename +' '

	cmd += settings['outputpath'] + id + '640.gif'
	if foundpics > 1:
		os.system(cmd)
		print '[convert] ' + cmd
	else:
		print '[convert] Only one pic!'
		os.system('mv '+settings['uploadpath']+id+'_1_img.jpg ' + settings['outputpath'] )

