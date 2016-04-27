import socket
import time
import requests
import subprocess
from screen import Screen

class Wifi(Screen):

    def __init__(self, hat):
        self.hat = hat
        self.cmd = ["iwlist", "wlan0", "scan"]
        self.last = 0

    def up(self):
        return "Diagnostics"
    def down(self):
        return "BinaryClock"

    def getQuality(self):
        proc = subprocess.Popen(self.cmd,stdout=subprocess.PIPE, universal_newlines=True)
        out,err = proc.communicate()
        for line in out.split("\n"):
            if "Quality" in line:
                line=line.strip(" ")
                line = line.split("S")[0].split("/")[0].split("=")[1]
                return int(line)

    def drawWifi(self, quality):
        green = [0,100,0]
        red=[100,0,0]
        blue=[0,0,100]
        self.hat.clear()
        if quality > self.last:
            self.hat.set_pixel(7,7,green)
        elif quality == self.last:
            self.hat.set_pixel(7,7,blue)
        else:
            self.hat.set_pixel(7,7,red)
        if quality == 0:
            self.hat.show_letter("X",red)
        if quality >= 15:
            self.hat.set_pixel(3,7,green)
            self.hat.set_pixel(4,7,green)
        if quality >= 30:
            self.hat.set_pixel(2,5,green)
            self.hat.set_pixel(3,5,green)
            self.hat.set_pixel(4,5,green)
            self.hat.set_pixel(5,5,green)
        if quality >= 45:
            self.hat.set_pixel(1,3,green)
            self.hat.set_pixel(2,3,green)
            self.hat.set_pixel(3,3,green)
            self.hat.set_pixel(4,3,green)
            self.hat.set_pixel(5,3,green)
            self.hat.set_pixel(6,3,green)
        if quality >= 60:
            self.hat.set_pixel(0,1,green)
            self.hat.set_pixel(1,1,green)
            self.hat.set_pixel(2,1,green)
            self.hat.set_pixel(3,1,green)
            self.hat.set_pixel(4,1,green)
            self.hat.set_pixel(5,1,green)
            self.hat.set_pixel(6,1,green)
            self.hat.set_pixel(7,1,green)

    def run(self, going):
        while going.isSet():
            #self.hat.clear()
            q = self.getQuality()
            self.drawWifi(q)
            self.last = q
            self.delay(5, going)

#if __name__ == "__main__":
#    import sense_hat
#    hat = sense_hat.SenseHat()
#    wifi = Wifi(hat)
#    while True:
#        q = wifi.getQuality()
#        wifi.drawWifi(q)
#        wifi.last = q
#        time.sleep(5)
