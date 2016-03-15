import socket
import time
import requests
from screen import Screen

class IpAddress(Screen):

    def __init__(self, hat):
        self.hat = hat

    def down(self):
        return "BinaryClock"
    
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
            self.hat.show_message("No IP", scroll_speed=0.25, text_colour=[100,0,0])

    def run(self, going):
        while going.isSet():
            self.printWan()
            time.sleep(2)
