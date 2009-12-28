known_triggers = []
def register_trigger(trigger_class):
  known_triggers.append(trigger_class)

def triggers_by_name():
  data = {}
  for i in known_triggers:
    data[i.__name__] = i
  return data

import LocationChanged
import TimeChanged
