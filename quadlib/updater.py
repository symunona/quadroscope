import utils
import json, socket, os, time
import convert

settings = None


root = os.path.dirname(__file__) + '/'

def myip():
	return ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])


class Updater:

    instance = None

    def __init__(self, settingso, camerano, boss):
        global settings
        self.instance = self
        self.settings = settingso
        settings = settingso
        self.camerano = camerano
        self.boss = boss
        files = json.load(open(os.path.join(root, 'sync.json')))
        
        def withroot(r): return root + r
         
        self.files_to_sync = ' '.join(map(withroot, files))                 
        self.employees = json.load(open(os.path.join(root, '../config/employees.json')))          
        #self.push()
        
    def send_to_all(self, cmd):
        for emp in self.employees:
            ip = employees[emp]['ip']
            cmdd = 'sshpass -p "' + self.settings["sshpasswd"] + '"' + cmd + '"'
            try:
                os.system(cmde)
            except OSError, e:
                print "[sync] error running '%s' " % cmde, e 
        
    def shutdown(self):
        self.send_to_all('sudo shutdown')
        
    def get_next_file_id(self):
        
        camsettings = utils.load_camera_settings()
        id = camsettings['nextid'] 
        print '[img id ]', id
        camsettings['nextid'] = int(camsettings['nextid']) + 1
        utils.save_camera_settings(camsettings)
        
        return id
                

    def get_output_file_name_for_id(self, id):
        return self.settings['uploadpath'] +'img-'+ '%04d' % id + '.gif'

    def pushToEmployee(self, no, ip):
        
        cmd = 'pkill -f camera.py'
        cmde = 'sshpass -p "' + self.settings["sshpasswd"] + '" ssh '+self.settings["sshusername"] +'@'+ip+' "'+cmd+'"'

        
        try:
            os.system(cmde)
        except OSError, e:
            print "[sync] error running '%s' " % cmde, e
                
        print "[sync] Updating " + str(no) + " @" + ip	
        cmd = "" 
        cmd += "mkdir -p " + self.settings["sshpath"]+'percamconfig/; '
        cmd += "cd " + self.settings["sshpath"]+'percamconfig/; '
        cmd += "echo "+no+" > camerano; "
        cmd += "echo '" + myip() + "' > bossip; "
            
        cmde = 'sshpass -p "' + self.settings["sshpasswd"] + '" ssh '+self.settings["sshusername"] +'@'+ip+' "'+cmd+'"'

        try:
            os.system(cmde)
        except OSError, e:
            print "[sync] error running '%s' " % cmde, e
                
        print "[sync] sending files " + self.files_to_sync
        
        upload_cmd = 'sshpass -p "' + self.settings["sshpasswd"] + '" scp -r '+self.files_to_sync+' '+self.settings["sshusername"] + '@'+ ip + ':' + self.settings["sshpath"]		
        print upload_cmd
        os.system(upload_cmd)


    def restart_employee(self, ip):
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

    def upload_photos(self, ip, file):
        os.system('sshpass -p "' + self.settings["sshpasswd"] + '" scp '+ self.settings["uploadpath"] + file+ ' '+self.settings["sshusername"] + '@'+ ip + ':' + '/' + self.settings["uploadpath"] )


    def download_photos(self, ip, file, target):
        os.system('sshpass -p "' + self.settings["sshpasswd"] + '" scp '+self.settings["sshusername"] + '@'+ ip + ':' + '/' + self.settings["uploadpath"] + file + ' /' + self.settings["uploadpath"] + target )


    def download_files_from_clients(self, id):
        
        for emp in self.employees.keys():
            remote_file_name = utils.get_file_name_for_id( id, emp )
            self.download_photos(self.employees[emp]['ip'], remote_file_name, remote_file_name)
        

    def wait_for_files_from_clients( self, id, camerasettings ):
        print "[convert] waiting for files of " + str(id)
                
        #lol, good enough for the demo...
        time.sleep(2)

        self.download_files_from_clients(id)
        
        convert.create_gif(id, self.employees, self.settings, camerasettings)

    # def upload_photo(self, file, ip):
    #     os.system('sshpass -p "' + self.settings["sshpasswd"] + '" scp '+file+' '+self.settings["sshusername"] + '@'+ ip + ':' + '/' + self.settings["uploadpath"])
        
