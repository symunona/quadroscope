#
# Quadroscope employee updater
#
# This file sends the new codebase to the employees and restarts the code.

import utils
import json, socket, os, time, thread, threading
import convert
import subprocess

settings = None

root = os.path.dirname(__file__) + '/'


# Returns the current user's IP
def myip():
    try:
        return ([
            l for l in (
                [
                    ip
                    for ip in socket.gethostbyname_ex(socket.gethostname())[2]
                    if not ip.startswith("127.")
                ][:1],
                [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close())
                  for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]
                  ][0][1]]) if l
        ][0][0])
    except:
        return ''


# Runs a command in bash.
def subprocess_cmd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    return proc_stdout


# Kills all python processes.
def clean_python():
    return 'sudo find . -name \'*.pyc\' -exec rm -rf {} ;'


class Updater:

    instance = None

    def __init__(self, camerano, boss, debug=False):
        global settings
        self.instance = self
        self.settings = utils.settings
        settings = utils.settings
        self.camerano = camerano
        self.boss = boss
        self.user = self.settings["sshusername"]
        files = json.load(open(os.path.join(root, 'sync.json')))

        #self.start_command = "sudo python " + self.settings["sshpath"] +'camera.py &'

        self.start_command = "sudo stdbuf -oL python " + self.settings["sshpath"] +'camera.py > /home/pi/kamera.log &'
        def withroot(r):
            return root + '../' + r

        self.files_to_sync = ' '.join(map(withroot, files))
        self.employees = json.load(
            open(os.path.join(root, '../config/employees.json')))

        # Update client code.
        if boss:
            if debug:
                utils.log( '[sync] DEBUG: updating clients')
                self.push()
            else:
                utils.log( '[sync] Restarting everyone...')
                self.restart_employees()
                self.sync_camera_settings()


    # Downloads/uploads files from an IP
    def download_files(self, ip, source, dest):
        return subprocess_cmd('scp ' + self.user + '@' + ip + ':' +
                          source + ' ' + dest)


    # Sends a ceratain command to one IP
    def send_to_one(self, cmd, ip):
        cmdd = 'ssh ' + self.user + '@' + ip + ' "' + cmd + '"'
        try:
            utils.log( '[sync] cmd: %s' % cmdd)
            utils.log( '[sync] res: %s' % subprocess_cmd(cmdd))
        except OSError, e:
            utils.log("[sync] error running '%s' " % cmdd, e)

    # Sends the given command to all the employees
    def send_to_all(self, cmd):
        for emp in self.employees:
            ip = self.employees[emp]['ip']
            if (ip == myip()): continue
            thread.start_new_thread(self.send_to_one, (cmd, ip))

    # Shuts the system down.
    def shutdown(self):
        self.send_to_all('sudo shutdown')
        os.system('sudo shutdown')

    # Reboots the system
    def reboot(self):
        self.send_to_all('sudo reboot')
        os.system('sudo reboot')

    # Increases the current file ID
    def step_file_id(self):
        camsettings = utils.load_camera_settings()
        id = camsettings['nextid']
        utils.log('[stepping]', id)
        camsettings['nextid'] = int(camsettings['nextid']) + 1
        utils.save_camera_settings(camsettings)

    # Reads next file ID from file.
    def get_next_file_id(self):
        camsettings = utils.load_camera_settings()
        id = camsettings['nextid']
        utils.log('[img id ]', id)
        return id

    # Generates the gif file name.
    def get_output_file_name_for_id(self, id):
        return self.settings['uploadpath'] + 'img-' + '%04d' % id + '.gif'

    def pushToEmployee(self, no, ip):
        
        cmd = 'sudo pkill -f camera.py; '        
        cmd += clean_python()
        cmd += "mkdir -p " + self.settings["sshpath"] + 'percamconfig/; '
        cmd += "cd " + self.settings["sshpath"] + 'percamconfig/; '
        cmd += "echo " + no + " > camerano; "
        cmd += "echo '" + myip() + "' > bossip; "

        cmde = 'ssh ' + self.user + '@' + ip + ' "' + cmd + '"'

        # utils.log('[sync] cmde: ', cmde)
        utils.log('[sync] res clean and config: ', subprocess_cmd(cmde))

        # utils.log("[sync] sending files " + self.files_to_sync)

        upload_cmd = 'scp -r ' + self.files_to_sync + ' ' + self.user + '@' + ip + ':' + self.settings["sshpath"]
        # utils.log(upload_cmd)
        utils.log('[sync] res upload: ', subprocess_cmd(upload_cmd))

        self.restart_employee(ip)

    def restart_employees(self):
        self.send_to_all("sudo pkill -f camera.py")
        self.send_to_all(self.start_command)

    def restart_employee(self, ip):
        restartscript = "ssh " + self.settings[
                "sshusername"] + '@' + ip + ' '
        restartscript += '"' + self.start_command + '"'
        utils.log('[sync] [restart] %s', ip, subprocess_cmd(restartscript))

    def push(self):
        utils.log("[sync] sending files to the other PIs")
        for emp in self.employees.keys():
            ip = self.employees[emp]['ip']

            if myip() != ip:
                # thread.start_new_thread( self.pushToEmployee, (emp, ip))
                self.pushToEmployee(emp, ip)
            else:
                utils.log("[sync] That's me: " + ip)
                settings["sshpath"] + '/percamconfig/; '
                os.system("echo 0 > " + self.settings["sshpath"] +
                          'percamconfig/camerano ')

    def pull(self):
        utils.log("[sync] getting settings from boss")
        bossip = open(root + '../percamconfig/bossip', 'r').read().strip('\n')
        source = root + '../config/camerasettings.json'
        dest = root + '../config/'
        res = self.download_files(bossip, source, dest)
        utils.log(res)

    def sync_camera_settings(self):
        threads = []
        for emp in self.employees:
            ip = self.employees[emp]['ip']
            cmd = 'scp ' + root + '/../config/camerasettings.json ' + self.settings[
                    "sshusername"] + '@' + ip + ':' + self.settings["sshpath"] + 'config'
            utils.log('[sync] updating camera ', str(emp))
            t = threading.Thread(target=subprocess_cmd, args=(cmd, ))
            t.start()
            threads.append(t)
            #subprocess_cmd(cmd)
        i = 0
        for t in threads:
            t.join()
            utils.log('[sync] updated camera ', str(i))
            i += 1
        return

    def upload_photos(self, ip, file):
        os.system('scp ' +
                  self.settings["uploadpath"] + file + ' ' +
                  self.user + '@' + ip + ':' + '/' +
                  self.settings["uploadpath"])

    def download_photos(self, ip, file, target):
        os.system('scp ' +
                  self.user + '@' + ip + ':' + file + ' /' +
                  target)

    def status(self):
        threads = []
        for emp in self.employees:
            ip = self.employees[emp]['ip']
            cmd = 'ssh ' + self.user + '@' + ip + ' "uptime"'
            utils.log('[sync] Camera Status: ' + ip + str(emp))
            t = threading.Thread(target=subprocess_cmd, args=(cmd, ))
            t.start()
            threads.append(t)
        i = 0
        for t in threads:
            t.join()
            utils.log('[sync] Camera Status: ', i, ': ', str(t))
            i += 1
        return

    def download_files_from_clients(self, id):

        for emp in self.employees.keys():
            remote_file_name = utils.get_file_name_for_id(id, emp)
            self.download_photos(self.employees[emp]['ip'], remote_file_name,
                                 remote_file_name)

    def wait_for_files_from_clients(self, id, camerasettings):
        utils.log("[convert] waiting for files of " + str(id))

        #lol, good enough for the demo...
        time.sleep(5)

        self.download_files_from_clients(id)

        convert.create_gif(id, self.employees, self.settings, camerasettings)

    # def upload_photo(self, file, ip):
    #     os.system('scp '+file+' '+self.user + '@'+ ip + ':' + '/' + self.settings["uploadpath"])
