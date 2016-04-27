from screen import Screen
from loading import LoadingScreen
import requests
import datetime
import time
import threading
import logging

class Buses(Screen):
    app_key = "2cb8993ac53cdf432e11556ac1d480eb"
    app_id = "7f77bbc8"
    stop_66 = "3290YYA03633"
    stop_44 = "3290YYA03608"
    address = "http://transportapi.com/v3/uk/bus/stop/{0}/live.json?app_id={1}&app_key={2}&group=route&nextbus=yes"

    def __init__(self, hat):
        self.requests = 0
        self.hat = hat
        self.ls = LoadingScreen(self.hat)
        self.notReady = threading.Event()
        self.refetch = True

    def left(self):
        return "BinaryClock"

    def request(self, stop):
        addr = self.address.format(stop, self.app_id, self.app_key)
        try:
            ret = requests.request('GET', addr, timeout=5)
            return ret.json()
        except requests.exceptions.Timeout as e:
            return "Timed out"
        return "Request failed"

    def timeToNext(self, time):
        now = datetime.datetime.now()
        time = time.split(":")
        hr = int(time[0])
        mins = int(time[1])
        if now.hour != hr:
            mins += 60
        nxt = mins - now.minute
        if nxt <= 0:
            self.refetch = True
        if nxt == 1:
            return str(nxt)+"min"
        else:
            return str(nxt)+"mins"

    def parse(self, data, bus):
        next_bus = data["departures"][bus][0]
        now = datetime.datetime.now()
        if next_bus.has_key("best_departure_estimate"):
            time = next_bus["best_departure_estimate"]
            return self.timeToNext(time)
        else:
            time = next_bus["expected_departure_time"]
            if time == "null":
                time = next_bus["aimed_departure_time"]
            if time == "null":
                return "No Data"
                self.refetch = True
            return self.timeToNext(time)

    def loadData(self):
        self.notReady.set()
        loading = threading.Thread(target=self.ls.run, args=(self.notReady,))
        loading.start()
        data66 = self.request(self.stop_66)
        data44 = self.request(self.stop_44)
        self.notReady.clear()
        loading.join()
        self.refetch = False
        return (("66", data66), ("44", data44))

    def display(self, time, bus):
        self.hat.show_message(bus+":"+time, scroll_speed=0.1, text_colour=[100,0,0])
        
    def run(self, going):
        while going.isSet():
            if self.refetch:
                data = self.loadData()
            for b,d in data:
                self.display(self.parse(d, b), b)
                if not going.isSet():
                    break
            if going.isSet():
                self.delay(2, going)
