import json, socket, os

root = os.path.dirname(__file__)

def myip():
	return ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])


class Updater:
    def __init__(self, self.settings):
        self.self.settings = self.settings
        self.files_to_sync = ' '.join(json.load(open(os.path.join(root, 'sync.json'))))                 
        self.employees = json.load(open(os.path.join(root, '../config/employees.json')))
        
        
    def distribute_next_file_id():

    def get_next_file_id(boss):

    def pushToEmployee(self, no, ip):
        
        cmd = 'pkill -f camera.py'
        cmde = 'sshpass -p "' + self.settings["sshpasswd"] + '" ssh '+self.settings["sshusername"] +'@'+ip+' "'+cmd+'"'
        os.system(cmde)

        print "[sync] Updating " + str(no) + " @" + ip	
        cmd = "" 
        cmd += "mkdir -p " + self.settings["sshpath"]+'percamconfig/; '
        cmd += "cd " + self.settings["sshpath"]+'percamconfig/; '
        cmd += "echo "+no+" > camerano; "
        cmd += "echo '" + myip() + "' > bossip; "
            
        cmde = 'sshpass -p "' + self.settings["sshpasswd"] + '" ssh '+self.settings["sshusername"] +'@'+ip+' "'+cmd+'"'

        os.system(cmde)

        print "[sync] sending files " + self.files_to_sync		
        os.system('cd '+root+'/.. ;sshpass -p "' + self.settings["sshpasswd"] + '" scp -r '+self.files_to_sync+' '+self.settings["sshusername"] + '@'+ ip + ':' + self.settings["sshpath"])


    def restart_employee(self):
        restartscript = "sshpass -p '" + self.settings["sshpasswd"] + "' ssh "+self.settings["sshusername"] +'@'+ip+' "'
        restartscript += "python " + self.settings["sshpath"] +'camera.py > /home/pi/kamera.log & "'
        os.system(restartscript)

    def push(self):
        print "[sync] sending files to the other PIs"
            for emp in self.employees.keys(): 
                ip = self.employees[emp]['ip']
                
                if myip() != ip:
                    self.pushToEmployee(emp, ip)
                else:
                    print "[sync] That's me: " + ip
                    settings["sshpath"]+'/percamcoonfig/; '
                    os.system("echo " + emp + ' > ' + self.settings["sshpath"]+'percamconfig/camerano ')
        
                        
    def sync_camera_settings(self):
        
        for emp in self.employees:
            ip = employees[emp]['ip']
            cmd = 'sshpass -p "' + self.settings["sshpasswd"] + '" scp '+ root + '/../config/cameraself.settings.json ' + self.settings["sshusername"] +'@'+ip+':'+self.settings["sshpath"]+'config'
            os.system(cmd)
        return 

    def uploadPhoto(file, ip, self.settings):
        os.system('sshpass -p "' + self.settings["sshpasswd"] + '" scp '+file+' '+self.settings["sshusername"] + '@'+ ip + ':' + '/' + self.settings["uploadpath"])
        
