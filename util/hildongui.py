from gi.repository import GUPnP, GUPnPAV
import pygtk
pygtk.require('2.0')
import gtk, gobject, hildon

from controllers.TriggerMaster import TriggerMaster
from util import inputs as inpututils
from util.action import UPnPAction
from util.autoremotegui import AutoRemoteGUI

class HildonAutoRemoteUI(AutoRemoteUI):
    
    def __init__(self, upnp_backend):
        super(HildonAutoRemoteUI, self).__init__(upnp_backend)
        
        self.window = hildon.StackableWindow()
        self.window.set_border_width(10)
        self.window.set_default_size(800,480)

        self.set_view("summary")
        self.window.show()

    def build_trigger_action_view(self):
        """
        Build a panel that will contain a list of all the
        already defined triggers in a HildonPannableView
        with a TreeView underneath        
        """
        
        tree_model = gtk.ListStore(str)
        treeview = gtk.TreeView(tree_model)
        
        col = gtk.TreeViewColumn("Triggers")
        col.cell = gtk.CellRendererText()
        col.pack_start(col.cell)
        col.set_attributes(col.cell, text=0)
        treeview.append_column(col)
        treeview.show()

        self.trigger_action_view = hildon.PannableArea()
        self.trigger_action_view.pack_start(treeview)
        self.trigger_action_view.show()
        
        return self.trigger_action_view
