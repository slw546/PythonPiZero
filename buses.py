from screen import Screen
from loading import LoadingScreen
import requests
import datetime
import time
import threading

class Buses(Screen):
    app_key = "2cb8993ac53cdf432e11556ac1d480eb"
    app_id = "7f77bbc8"
    stop_66 = "3290YYA03633"
    stop_44 = "3290YYA03608"
    address = "http://transportapi.com/v3/uk/bus/stop/{0}/live.json?app_id={1}&app_key={2}&group=route&nextbus=yes"
    max_requests = 1000

    def __init__(self, hat):
        self.requests = 0
        self.initialised = datetime.datetime.now()
        self.renew = self.initialised + datetime.timedelta(days=1)
        self.hat = hat
        self.last_request = self.initialised - datetime.timedelta(days=1)
        self.current_44 = None
        self.current_66 = None
        self.ls = LoadingScreen(self.hat)
        self.notReady = threading.Event()
        self.newThread()

    def newThread(self):
        self.loading_screen = threading.Thread(target=self.ls.run, args=(self.notReady,))

    def left(self):
        return "BinaryClock"

    def check_request(self):
        if (self.requests+1) > self.max_requests:
            return False
        return True

    def renew_requests(self):
        now = datetime.datetime.now()
        if now > self.renew:
            self.initialised = self.renew
            self.renew = self.initalised + datetime.timedelta(days=1)
            self.requests = 0

    def inc_requests(self):
        self.requests = self.requests + 10

    def get_json(self, addr):
        self.last_request = datetime.datetime.now()
        ret_str = requests.request('GET', addr)
        return ret_str.json()

    def request_66(self):
        self.renew_requests()
        if self.check_request():
            addr = self.address.format(self.stop_66, self.app_id, self.app_key)
            self.current_66 = self.get_json(addr)
            self.inc_requests()

    def request_44(self):
        self.renew_requests()
        if self.check_request():
            addr = self.address.format(self.stop_44, self.app_id, self.app_key)
            self.current_44 = self.get_json(addr)
            self.inc_requests()

    def current_data_valid(self):
        window = self.last_request + datetime.timedelta(minutes=5)
        now = datetime.datetime.now()
        if window > now:
            return True
        return False

    def show(self, data, bus):
        departures = data["departures"][bus]
        next_time = departures[0]["best_departure_estimate"].split(":")
        hr = int(next_time[0])
        mins = int(next_time[1])
        now = datetime.datetime.now()
        if now.hour != hr:
            mins += 60
        time_til_next = mins - now.minute
        if time_til_next == 1:
            nxt = str(time_til_next)+"min"
        else:
            nxt = str(time_til_next)+"mins"
        self.hat.show_message(bus + ":" + nxt, scroll_speed=0.1, text_colour=[100,0,0]) 

    def run(self, going):
        once = False
        while going.isSet():
            if not self.current_data_valid():
                self.newThread()
                self.notReady.set()
                self.loading_screen.start()
                self.request_66()
                self.request_44()
                self.notReady.clear()
                self.loading_screen.join()
            self.show(self.current_66, "66")
            if not going.isSet():
                continue
            self.show(self.current_44, "44")
            if going.isSet():
                time.sleep(1)
