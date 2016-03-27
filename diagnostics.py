import socket
import time
import requests
import psutil
import os
from screen import Screen

class Diagnostics(Screen):

    def __init__(self, hat):
        self.hat = hat
        self.cpu_usage = psutil.cpu_percent()

    def down(self):
        return "IpAddress"
    
    def getLocalIp(self):
        return socket.gethostbyname(socket.getfqdn())

    def printLocalIp(self):
        self.hat.show_message(self.getLocalIp(), scroll_speed=0.1, text_colour=[100,0,0])

    def getWan(self):
        ret = requests.request('GET', 'http://myip.dnsomatic.com')
        return ret.text

    def printWan(self):
        try:
            self.hat.show_message(self.getWan(), scroll_speed=0.1, text_colour=[100,0,0])
        except Exception as e:
            self.hat.show_message("No IP", scroll_speed=0.1, text_colour=[100,0,0])

    def printCpuUsage(self):
        cpu = psutil.cpu_percent(interval=1)
        self.hat.show_message("CPU: "+str(cpu)+"%", scroll_speed=0.1, text_colour=[100,0,0])

    def printCpuTemp(self):
        cpu_temp = os.popen('/opt/vc/bin/vcgencmd measure_temp').read()
        cpu_temp = cpu_temp.replace("temp=","")
        self.hat.show_message("CPU Temp: " + cpu_temp, scroll_speed=0.1, text_colour=[100,0,0])

    def printDiskUsage(self):
        percent = psutil.disk_usage('/').percent
        self.hat.show_message("Disk: "+str(percent)+"%", scroll_speed=0.1, text_colour=[100,0,0])

    def run(self, going):
        while going.isSet():
            self.printCpuUsage()
            self.delay(2, going)
            self.printCpuTemp()
            self.delay(2, going)
            self.printDiskUsage()
            self.delay(2, going)
            self.printWan()
            self.delay(2, going)
