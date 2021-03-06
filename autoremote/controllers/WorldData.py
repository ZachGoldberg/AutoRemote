import physics 
class WorldState(object):
  """
   A struct which contains information about the world at one given time
  """
  def __init__(self):
      self.time = None
      self.wifi_location = None
      self.battery_level = None
      self.gps_location = None

  def set_time(self, datetime):
      self.time = datetime

  def get_time(self):
      return self.time     

  def set_wifi_location(self, wifi_location):
      """
      @param wifi_location a python-wifi wireless network object
      """
      self.wifi_location = wifi_location

  def get_wifi_location(self):
      return self.wifi_location

class WorldData(object):
  """
    A struct which contains information about the world over time
  """
  def __init__(self):
      self.timesteps = []      

  def advance_time(self):
      thepresent = WorldState()
      for law in physics.known_physics_laws:
        law.run(thepresent, self)
      self.add_timestep(thepresent)
      
  def add_timestep(self, worldstate):
      self.timesteps.append(worldstate)

  def now(self, offset=0):
      return self.timesteps[-1 + offset]
