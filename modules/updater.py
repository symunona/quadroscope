import json, socket, os

def myip():
	return ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
	
def pushToEmployee(no, ip, settings):
	print "[sync] Updating " + str(no) + " @" + ip	

	os.system('sshpass -p "' + settings["sshpasswd"] + '" ssh pi@'+ip+' "echo '+no+' > camerano"')

	with open('sync.json') as syncfilelistfile:
                files = json.load(syncfilelistfile)
		for file in files:
			print "[sync] sending " + file		
			os.system('sshpass -p "' + settings["sshpasswd"] + '" scp '+file+' '+settings["sshusername"] + '@'+ ip + ':' + settings["sshpath"])
			

def uploadPhoto(file, settings):
	os.system('sshpass -p "' + settings["sshpasswd"] + '" scp '+file+' '+settings["sshusername"] + '@'+ ip + ':' + '/' + settings["uploadpath"])
	


def push(sshsettings):
	print "[sync] sending files to the other PIs"
	with open('employers.json') as employeefile:    
		employees = json.load(employeefile)
		for emp in employees.keys(): 
			ip = employees[emp]
			
			if myip() != ip:			
				pushToEmployee(emp, ip, sshsettings)
			else:
				print "[sync] That's me: " + ip

			#print "myip " + myip() + " ip " + ip + " equals: " + str(myip() != ip)
