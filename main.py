from sense_hat import SenseHat
from binary_clock import BinaryClock
from room_conditions import RoomConditions
from ip_address import IpAddress
from buses import Buses
from loading import LoadingScreen
from diagnostics import Diagnostics

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
        self.binary_clock = BinaryClock(self.hat)
        self.room_conditions = RoomConditions(self.hat)
        self.binary_clock.setRC(self.room_conditions)
        self.ip_addr = IpAddress(self.hat)
        self.buses = Buses(self.hat)
        self.loading = LoadingScreen(self.hat)
        self.diagnostics = Diagnostics(self.hat)
        for d in devices:
            if d.name == "Raspberry Pi Sense HAT Joystick":
                self.stick = d
                print "found "+d.name
                break

    def getScreen(self, code):
        if code == "BinaryClock":
            return self.binary_clock
        elif code == "RoomConditions":
            return self.room_conditions
        elif code == "IpAddress":
            return self.ip_addr
        elif code == "Buses":
            return self.buses
        elif code == "Loading":
            return self.loading
        elif code == "Diagnostics":
            return self.diagnostics
        return self.binary_clock

    def handle_event(self, event):
        code = event.code
        scr = None
        if code == ecodes.KEY_DOWN:
            scr = self.screen.down()
        elif code == ecodes.KEY_UP:
            scr = self.screen.up()
        elif code == ecodes.KEY_LEFT:
            scr = self.screen.left()
        elif code == ecodes.KEY_RIGHT:
            scr = self.screen.right()
        elif code == ecodes.KEY_ENTER:
            self.screen.press()
        if scr:
            # Change to new screen
            scr = self.getScreen(scr)
            self.move_to_screen(scr)
            self.start_screen()
    
    def move_to_screen(self, newScreen):
        #Close old screen
        self.going.clear()
        if self.screen_thread:
            self.screen_thread.join()

        self.screen = newScreen
        self.screen_thread = threading.Thread(target=self.screen.run, args=(self.going,))

    def start_screen(self):
        self.going.set()
        self.screen_thread.start()

    def run(self):
        self.move_to_screen(self.getScreen("BinaryClock"))
        self.start_screen()
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
            main_going=False
            print "keyboard interrupt"
            self.going.clear()
            print "waiting for thread to clean up"
            time.sleep(5)
            print "exit"
        except Exception as e:
            print e

if __name__ == "__main__":
    main = Main()
    main.run()
