from sense_hat import SenseHat
from binary_clock import BinaryClock
from room_conditions import RoomConditions

class Main:
    def __init__(self):
        self.hat = SenseHat()
        self.hat.set_rotation(90)
        self.hat.clear()
        self.screen = BinaryClock(self.hat)

    def run(self):
        self.screen.run()

if __name__ == "__main__":
    main = Main()
    main.run()
