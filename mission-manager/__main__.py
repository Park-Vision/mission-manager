from transitions import Machine

from drone import Drone, DroneStates
    

transitions = [ #TODO
    { 'trigger': 'get_ready', 'source': DroneStates.INITIALIZING, 'dest': DroneStates.READY },
    { 'trigger': 'evaporate', 'source': 'liquid', 'dest': 'gas' },
    { 'trigger': 'sublimate', 'source': 'solid', 'dest': 'gas' },
    { 'trigger': 'ionize', 'source': 'gas', 'dest': 'plasma' }
]

if __name__ == "__main__":
    drone = Drone()
    state_machine = Machine(model=drone, states=DroneStates, initial=DroneStates.INITIALIZING, transitions=transitions)
    drone.get_ready()
