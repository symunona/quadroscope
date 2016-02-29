import convert
import time

def make_photos(updater, fileid, filename):

    # if boss, then upload settings to other cameras
    if isBoss:
        triggerEmployees( True )
            
    camera.take_picture(filename)
            
    if isBoss:
        triggerEmployees(False)
        print "[listener] i is the boss, creating gif..."
        thread.start_new_thread( convert.download_files_from_clients, (updater, fileid, settings, camera_settings, ))		
    
    # mode 1: it downloads the files 
    # if not isBoss:
    #     print "[listener] i am an employee. Uploading image to boss@" + bossip		
    #     updater.upload_photo(filename, bossip, settings)

    print("[listener] Picture took. Listening.")


def camera_loop(updater, gpio, camera):
    
    while True:

        fileid = updater.get_next_file_id()
        
        filename = updater.get_file_name_for_id(fileid)
        
        gpio.wait_for_trigger()                     # ____/
    
        make_photos(updater, fileid, filename)       # break break
        
        gpio.wait_for_release()                     #     \____
        
        


def download_files_from_clients( updater, id ):
    print "[convert] waiting for files of " + id

    #lol, good enough for the demo...
    time.sleep(6)

    updater.download_files_from_clients(id)

    createGif(id)

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

