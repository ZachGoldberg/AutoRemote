from PhysicsLaw import PhysicsLaw
import physics
from wifiloc import WifiLoc

class WifiLocationPhysics(PhysicsLaw):
    """ The Physics of Changing Wifi Locations! """
    def __init__(self):
        self.wifiloc = WifiLoc()
    
    def initial_state(worldstate):
        worldstate.wifi_location = None
        worldstate.get_wifi_location = get_wifi_location
        worldstate.set_wifi_location = set_wifi_location
        return worldstate

    def get_wifi_location(self):
        return self.wifi_location

    def set_wifi_location(self, wifi_location):
        self.wifi_location = wifi_location
    
    def run(self, worldstate, world):
        self.wifiloc.update_location()
        worldstate.set_wifi_location(self.wifiloc.getCurrentAP())    
        return worldstate

physics.learn_law(WifiLocationPhysics)
