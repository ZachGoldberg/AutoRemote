from gi.repository import GUPnP, GUPnPAV
import pygtk
pygtk.require('2.0')
import gtk, gobject

from controllers.TriggerMaster import TriggerMaster
from util import inputs as inpututils
from util.action import UPnPAction
from util.autoremotegui import AutoRemoteGUI

class GTKAutoRemoteUI(AutoRemoteUI):

    def __init__(self, upnp_backend):
        super(GTKAutoRemoteUI, self).__init__(upnp_backend)
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)    
        self.window.set_border_width(10)
        self.window.set_default_size(800,480)

        self.set_view("summary")
        self.window.show()

