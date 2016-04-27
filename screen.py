import time

class Screen:
    def __init__(self):
        pass

    def up(self):
        pass

    def down(self):
        pass

    def left(self):
        pass

    def right(self):
        pass

    def press(self):
        pass

    def run(self):
        pass

    def delay(self, t, going):
        if t == 0:
            return
        else:
            if going.isSet():
                time.sleep(1)
                self.delay(t-1, going)
            else:
                return

