from util.action import UPnPAction
import simplejson, triggers

class Trigger(object):

   unserializable_fields = ["action", "displayName"]
   
   def __init__(self, triggerdata):
      for key, value in triggerdata.items():
          setattr(self, key, value)

      if isinstance(triggerdata["upnpaction"], basestring):
         self.action = UPnPAction.loads(triggerdata["upnpaction"])
      else:
         self.action = triggerdata["upnpaction"]
         self.upnpaction = self.action.dumps()

      if not hasattr(self, "reusable"):
         self.reusable = False

      self.active = True

   def get_name(self):
      if not hasattr(self, "name") or not self.name:
         return "Basic Trigger"
      else:
         if hasattr(self, "displayName"):
            return self.displayName
         else:
            return self.name

   def is_triggered(self, world_data):
      return False

   def execute_action(self):
      """
      It may make good sense for a trigger to override this function
      and modify the state of the trigger based upon whether or not the
      trigger could actually be run (action.is_executable())   
      """
      if self.action.is_executable():
         self.action.execute()

   def dumps(self):
      data = self.__dict__.copy()
      for field in Trigger.unserializable_fields:
         if field in data:
            del data[field]

      return simplejson.dumps(data)

   @classmethod
   def loads(clz, str):
      if isinstance(str, basestring):
         data = simplejson.loads(str)
      else:
         data = str

      if not Trigger.check_valid_triggerdata(data):
         raise Exception("Invalid Trigger Found (%s)" % data)
         
      clzname = data["trigger_class"]
      return triggers.triggers_by_name()[clzname](data)

   @classmethod
   def check_valid_triggerdata(clz, triggerdict):
      return set([u"upnpaction", u"trigger_class"]).issubset(
         set(triggerdict.keys()))
