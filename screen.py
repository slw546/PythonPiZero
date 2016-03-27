import time

class Screen:
    def __init__(self):
        pass

    def up(self):
        return "None"

    def down(self):
        return "None"

    def left(self):
        return "None"

    def right(self):
        return "None"

    def press(self):
        pass

    def run(self):
        pass

    def delay(self, t, going):
        if t is 0:
            return
        else:
            if going.isSet():
                time.sleep(1)
                self.delay(t-1, going)
            else:
                return

