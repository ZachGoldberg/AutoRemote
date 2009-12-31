import simplejson

class UPnPAction(object):
    def __init__(self, device, service, action, data, next_action=False):
        
        if isinstance(device, basestring):
            self.device_udn = device
            self.device = None
        else:
            self.device = device
            self.device_udn = device.get_udn()

        if isinstance(service,  basestring):
            self.service_type = service
            self.service = None
        else:
            self.service = service
            self.service_type = service.get_service_type()

        self.action = action
        self.data = data

        self.next_action = next_action

    def activate(self, device, service):
        self.device = device
        self.service = service
        if self.is_activated():
            print "ACTIVATED"
        else:
            print "INACTIVATED"

        print self.device, self.service, 

    def execute(self):
        if self.is_executable():
            print "Send action"
            try:
                self.service.send_action_hash(str(self.action), self.data, {})
            except:
                print "Error sending action"
            print "Send action done"
        else:
            print "Error -- Tried to execute an action that hasn't been activated"
            
    def is_executable(self):
        return bool(self.service)

    is_activated = is_executable
    
    def dumps(self):
        next_action = None
        if self.next_action:
            next_action = self.next_action.dumps()
            
        return simplejson.dumps({
            "device": self.device_udn,
            "service": self.service_type,
            "action": self.action,
            "data": simplejson.dumps(self.data),
            "next_action": next_action,
                })

    @classmethod
    def loads(claz, datas):
        data = simplejson.loads(datas)
        next_action = None
        if "next_action" in data and data["next_action"]:
            next_action = UPnPAction.loads(data["next_action"])
            
        return UPnPAction(
            data["device"],
            data["service"],
            data["action"],
            simplejson.loads(data["data"])          
            )
