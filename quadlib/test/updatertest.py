# TEST SSH

cmd = 'ssh pi@emp4 "uname -a"'

# import commands
# print commands.getstatusoutput('ssh pi@emp1 "uname -a"')

import subprocess


def subprocess_cmd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    return proc_stdout


print subprocess_cmd(cmd)
