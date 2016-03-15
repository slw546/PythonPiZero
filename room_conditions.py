import os
import time

class RoomConditions:
    red = [100,0,0]
    def __init__(self, hat):
        self.hat = hat
        self.temp_history = [self.hat.get_temperature()]*8
        self.humidity_history = [self.hat.get_humidity()]*8
        self.pressure_history = [self.hat.get_pressure()]*8
        self.index = 0
    
    def up(self):
        return "BinaryClock"

    def getTemp(self):
        temp = self.hat.get_temperature()
        cpu_temp = os.popen('/opt/vc/bin/vcgencmd measure_temp').read()
        cpu_temp = cpu_temp.replace("temp=","")
        cpu_temp = cpu_temp.replace("\'C\n","")
        calc_temp = temp - (float(cpu_temp)-temp)/1.5
        self.temp_history[self.index]=calc_temp
        return "Room Temp: " + "{0:.1f}".format(calc_temp) + "\'C"

    def getHumidity(self):
        humidity = self.hat.get_humidity()
        self.humidity_history[self.index]=humidity
        return "Humidity: " + "{0:.1f}".format(humidity)+"%rH"

    def getPressure(self):
        pressure = self.hat.get_pressure()
        self.pressure_history[self.index]=pressure
        return "Pressure: " + "{0:.1f}".format(pressure)+" Millibars"

    def incIndex(self):
        self.index = (self.index +1) % 8
    
    def delay(self, t, going):
        if t is 0:
            return
        else:
            if going.isSet():
                time.sleep(1)
                self.delay(t-1, going)
            else:
                return

    def show(self, going):
        if going.isSet():
            self.hat.show_message(self.getTemp(), scroll_speed=0.1, text_colour=self.red)
            self.delay(2, going)
        if going.isSet():
            self.hat.show_message(self.getHumidity(), scroll_speed=0.1, text_colour=self.red)
            self.delay(2, going)
        if going.isSet():
            self.hat.show_message(self.getPressure(), scroll_speed=0.1, text_colour=self.red)
            self.delay(2, going)
        self.incIndex()

    def run(self, going):
        while going.isSet():
            self.show(going)
