from datetime import datetime

from PhysicsLaw import PhysicsLaw
import physics

class TimePhysics (PhysicsLaw):
    """ The Physics of Time! """
    def __init__(self):
        pass

    def initial_state(worldstate):
        worldstate.time = None
        worldstate.get_time = get_time
        worldstate.set_time = set_time
        return worldstate

    def get_time(self):
        return self.time

    def set_time(self, datetime):
        self.time = datetime

    def run(self, worldstate, world):
        worldstate.set_time(datetime.now())
        return worldstate

physics.learn_law(TimePhysics)
