from gi.repository import GLib, GUPnP, GSSDP, GObject, libsoup
from wifiloc import getCurrentAP

def device_available(device, cp):
  print cp

def run_timer():

  ap = getCurrentAP()

  print "Ran, best hotspot is: %s (%s)" % (ap.essid, ap.bssid)
  return True


# Note: glib.thread_init() doesn't work here, have to use the gobject call
GObject.threads_init()

# Get a default maincontext
main_ctx = GLib.main_context_default()

ctx = GUPnP.Context(interface="eth1")

# Bind to eth0 in the maincontext on any port
cp  = GUPnP.ControlPoint().new(ctx, "upnp:rootdevice")

# Use glib style .connect() as a callback on the controlpoint to listen for new devices
cp.connect("device-proxy-available", device_available)

# "Tell the Control Point to Start Searching"
GSSDP.ResourceBrowser.set_active(cp, True)

GObject.timeout_add(5000, run_timer)

# Enter the main loop which begins the work and facilitates callbacks
GObject.MainLoop().run()


