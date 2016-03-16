import datetime
import time
import sys
from screen import Screen
from room_conditions import RoomConditions

class BinaryClock(Screen):
    red = [100,0,0]
    off = [0,0,0]

    def right(self):
        return "Buses"
   
    def down(self):
        return "RoomConditions"

    def up(self):
        return "IpAddress"

    def press(self):
        self.pressed = not self.pressed

    def __init__(self, hat):
        self.hat = hat
        self.rc = RoomConditions(hat)
        self.clock_off = False
        self.pressed = False

    def setPixels(self, startX, startY, val):
        x = startX
        y = startY
        for char in val:
            if char is "1":
                self.hat.set_pixel(x,y,self.red)
                self.hat.set_pixel(x-1,y,self.red)
            else:
                self.hat.set_pixel(x,y,self.off)
                self.hat.set_pixel(x-1,y,self.off)
            y = y+1

    def tick(self, now):
        hour = "{0:06b}".format(now.hour)
        mins = "{0:06b}".format(now.minute)
        second = now.second
        secs = "{0:06b}".format(second)
        self.setPixels(1,1,hour)
        self.setPixels(4,1,mins)
        self.setPixels(7,1,secs)

    def run(self, going):
        temp_printed = False
        while going.isSet():
            now = datetime.datetime.now()
            clock_off = False
            if (now.hour >= 22) or (now.hour < 9):
                clock_off = True
            if clock_off:
                if not self.pressed:
                    self.hat.clear()
                    continue
            if (now.minute % 10) == 0:
                if not temp_printed:
                    self.rc.show(going)
                    now = datetime.datetime.now()
                    temp_printed = True
            else:
                temp_printed = False
            self.tick(now)
            next = 1000 - (now.microsecond/1000)
            time.sleep(float(next)/float(1000))

