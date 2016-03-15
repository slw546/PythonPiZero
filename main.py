from sense_hat import SenseHat
from binary_clock import BinaryClock
from room_conditions import RoomConditions
from ip_address import IpAddress

import threading
import time
from evdev import InputDevice, list_devices, ecodes

class Main:
    def __init__(self):
        self.hat = SenseHat()
        self.hat.set_rotation(90)
        self.hat.clear()
        self.screen = None
        devices = [InputDevice(d) for d in list_devices()]
        self.stick = None
        self.going = threading.Event()
        self.screen_thread = None
        for d in devices:
            if d.name == "Raspberry Pi Sense HAT Joystick":
                self.stick = d
                print "found "+d.name
                break

    def getScreen(self, code):
        if code == "BinaryClock":
            return BinaryClock(self.hat)
        elif code == "RoomConditions":
            return RoomConditions(self.hat)
        elif code == "IpAddress":
            return IpAddress(self.hat)

    def handle_event(self, event):
        code = event.code
        scr = None
        if code == ecodes.KEY_DOWN:
            scr = self.screen.down()
            print "d"
        elif code == ecodes.KEY_UP:
            scr = self.screen.up()
            print "u"
        elif code == ecodes.KEY_LEFT:
            scr = self.screen.left()
            print "l"
        elif code == ecodes.KEY_RIGHT:
            scr = self.screen.right()
            print "r"
        if scr:
            # Change to new screen
            scr = self.getScreen(scr)
            self.move_to_screen(scr)
            self.start_screen()
    
    def move_to_screen(self, newScreen):
        #Close old screen
        self.going.clear()
        if self.screen_thread:
            print "1"
            self.screen_thread.join()
        print "2"

        self.screen = newScreen
        self.screen_thread = threading.Thread(target=self.screen.run, args=(self.going,))
        print "3"

    def start_screen(self):
        self.going.set()
        self.screen_thread.start()

    def run(self):
        print "start"
        self.move_to_screen(self.getScreen("BinaryClock"))
        print "moved"
        self.start_screen()
        print "started"
        main_going = True
        try:
            while main_going:
                if self.stick:
                    for event in self.stick.read_loop():
                        if event.type == ecodes.EV_KEY:
                            if event.value == 1:
                                self.handle_event(event)
                time.sleep(1)
        except KeyboardInterrupt:
            self.going.clear()
            self.screen_thread.join()
        except Exception as e:
            print e

if __name__ == "__main__":
    main = Main()
    main.run()
