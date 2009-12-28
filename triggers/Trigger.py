

class Trigger(object):
   def __init__(self, triggerdata):
      for key, value in triggerdata.items():
          setattr(self, key, value)

   def is_triggered(world_data):
      return False
