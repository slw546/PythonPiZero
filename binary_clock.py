import datetime
import time
import sys
from room_conditions import RoomConditions

class BinaryClock:
    red = [100,0,0]
    off = [0,0,0]
    def __init__(self, hat):
        self.hat = hat
        self.rc = RoomConditions(hat)

    def setPixels(self, startX, startY, val):
        x = startX
        y = startY
        for char in val:
            if char is "1":
                self.hat.set_pixel(x,y,self.red)
            else:
                self.hat.set_pixel(x,y,self.off)
            y = y+1

    def tick(self, now):
        hour = "{0:06b}".format(now.hour)
        mins = "{0:06b}".format(now.minute)
        second = now.second
        secs = "{0:06b}".format(second)
        self.setPixels(1,1,hour)
        self.setPixels(3,1,mins)
        self.setPixels(5,1,secs)

    def run(self):
        going = True
        temp_printed = False
        while going:
            now = datetime.datetime.now()
            if now.hour >= 22:
                time.sleep(0.5)
                continue
            if (now.minute % 10) == 0:
                self.rc.show()
                now = datetime.datetime.now()
                temp_printed = True
            else:
                temp_printed = False
            self.tick(now)
            next = 1000 - (now.microsecond/1000)
            time.sleep(float(next)/float(1000))

