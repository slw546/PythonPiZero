from sense_hat import SenseHat
from binary_clock import BinaryClock
from room_conditions import RoomConditions
from wifi import Wifi
from buses import Buses
from loading import LoadingScreen
from diagnostics import Diagnostics
import bash

import threading
import time
from evdev import InputDevice, list_devices, ecodes, events

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
        self.wifi = Wifi(self.hat)
        self.buses = Buses(self.hat)
        self.loading = LoadingScreen(self.hat)
        self.diagnostics = Diagnostics(self.hat)
        self.hold_start = None
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
        elif code == "Wifi":
            return self.wifi
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

    def handle_hold(self, event):
        code = event.code
        if code == ecodes.KEY_ENTER:
            if self.hold_start is None:
                self.hold_start = time.time()
            now = time.time()
            down_time = now - self.hold_start
            if down_time > 5:
                self.going.clear()
                self.screen_thread.join()
                self.hat.clear()
                self.hat.show_message("Halting", scroll_speed=0.1, text_colour=[100,0,0])
                bash.shutdown()
    
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
                        now = time.time()
                        if self.hold_start is not None:
                            if now - self.hold_start > 6:
                                self.hold_start = None
                        event = events.KeyEvent(event)
                        if event.event.type == ecodes.EV_KEY:
                            if event.event.value == 1:
                                self.handle_event(event.event)
                            elif event.keystate == 2:
                                self.handle_hold(event.event)
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
