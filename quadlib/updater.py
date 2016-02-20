import json, socket, os

root = os.path.dirname(__file__)

def myip():
	return ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
	
def pushToEmployee(no, ip, settings):
	
	cmd = 'pkill -f camera.py'
	cmde = 'sshpass -p "' + settings["sshpasswd"] + '" ssh '+settings["sshusername"] +'@'+ip+' "'+cmd+'"'
	os.system(cmde)

	print "[sync] Updating " + str(no) + " @" + ip	
	cmd = "" 
	cmd += "mkdir -p " + settings["sshpath"]+'percamconfig/; '
	cmd += "cd " + settings["sshpath"]+'percamconfig/; '
	cmd += "echo "+no+" > camerano; "
	cmd += "echo '" + myip() + "' > bossip; "
		
	cmde = 'sshpass -p "' + settings["sshpasswd"] + '" ssh '+settings["sshusername"] +'@'+ip+' "'+cmd+'"'

	os.system(cmde)

	filelist = ' '

	with open(os.path.join(root, 'sync.json')) as syncfilelistfile:
                files = json.load(syncfilelistfile)
		filelist = filelist.join(files)
		print "[sync] sending files " + filelist		
		os.system('cd '+root+'/.. ;sshpass -p "' + settings["sshpasswd"] + '" scp -r '+filelist+' '+settings["sshusername"] + '@'+ ip + ':' + settings["sshpath"])

	restartscript = "sshpass -p '" + settings["sshpasswd"] + "' ssh "+settings["sshusername"] +'@'+ip+' "'
	restartscript += "python " + settings["sshpath"] +'camera.py > /home/pi/kamera.log & "'
	os.system(restartscript)

			
def syncCameraSettings(employees, settings):
	for emp in employees:
		ip = employees[emp]['ip']
		cmd = 'sshpass -p "' + settings["sshpasswd"] + '" scp '+ root + '/../config/camerasettings.json ' + settings["sshusername"] +'@'+ip+':'+settings["sshpath"]+'config'
		os.system(cmd)
	return 

def uploadPhoto(file, ip, settings):
	os.system('sshpass -p "' + settings["sshpasswd"] + '" scp '+file+' '+settings["sshusername"] + '@'+ ip + ':' + '/' + settings["uploadpath"])
	

def push(settings):
	print "[sync] sending files to the other PIs"
	with open(os.path.join(root, '../config/employees.json')) as employeefile:    
		employees = json.load(employeefile)
		for emp in employees.keys(): 
			ip = employees[emp]['ip']
			
			if myip() != ip:
				pushToEmployee(emp, ip, settings)
			else:
				print "[sync] That's me: " + ip
				settings["sshpath"]+'/percamcoonfig/; '
				os.system("echo " + emp + ' > ' + settings["sshpath"]+'percamconfig/camerano ')

			#print "myip " + myip() + " ip " + ip + " equals: " + str(myip() != ip)
	return employees
