import time

class LoadingScreen:
    red = [100,0,0]
    blue = [0,100,0]
    green = [0,0,100]

    def __init__(self, hat):
        self.hat = hat
        self.head = (1,1)
        self.body = [(2,1), (3,1), (4,1)]

    def show(self):
        self.hat.clear()
        self.hat.set_pixel(self.head[0], self.head[1], self.red)
        for coord in self.body:
            self.hat.set_pixel(coord[0], coord[1], self.red)

    def update(self):
        self.body[-1] = self.body[-2]
        self.body[-2] = self.body[-3]
        self.body[-3] = self.head
        if self.head == (1,1):
            self.head = (1,2)
        elif self.head == (1,6):
            self.head = (2,6)
        elif self.head == (6,6):
            self.head = (6,5)
        elif self.head == (6,1):
            self.head = (5,1)
        elif (self.head[0] == 1) and (self.head[1] < 6):
            self.head = (self.head[0], self.head[1]+1)
        elif (self.head[1] == 6) and (self.head[0] < 6):
            self.head = (self.head[0]+1, self.head[1])
        elif (self.head[0] == 6) and (self.head[1] > 1):
            self.head = (self.head[0], self.head[1]-1)
        elif (self.head[1] == 1) and (self.head[0] > 1):
            self.head = (self.head[0]-1, self.head[1])
            

    def run(self, notReady):
        while notReady.isSet():
            self.show()
            self.update()
            time.sleep(0.1)
            

    
