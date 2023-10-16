import enum

class DroneStates(enum.Enum):
    INITIALIZING = 0
    READY = 1
    PATH = 2
    TAKEOFF = 3
    FLIGHT = 4
    RTL = 5
    RAPORT = 6


class Drone(object):
    def on_enter_READY(self): 
        print("We've just entered state ready!")