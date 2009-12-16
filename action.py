import simplejson

class UPnPAction(object):
    def __init__(self, device, service, action, data):
        self.device_udn = device.get_udn()
        self.service_udn = service.get_udn()
        self.action = action
        self.data = data

    def dumps(self):
        return simplejson.dumps({
                "device": self.device_udn,
                "service": self.service_udn,
                "action": self.action,
                "data": simplejson.dumps(self.data)
                })

    @classmethod
    def loads(datas):
        data = simplejson.loads(datas)
        return UPnPAction(
            data["device"],
            data["service"],
            data["action"],
            simplejson.loads(data["data"])
            )
