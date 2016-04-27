import subprocess

def shutdown():
    command = "/usr/bin/sudo /sbin/shutdown now"
    proc = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = proc.communicate()[0]
    print output

def restart():
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    proc = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = proc.communicate()[0]
    print output
