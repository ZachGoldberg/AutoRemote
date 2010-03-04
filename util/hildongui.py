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
        treeview = super(HildonAutoRemoteUI, self).build_trigger_action_view()

        pannable = hildon.PannableArea()
        pannable.pack_start(treeview)
        pannable.show()
        
        return pannable

    def build_window_choser(self):
        """
        Add a list of option to the ui toolbar which chose what view to be in        
        """
        pass


    def build_trigger_creation_window(self):
        self.actions = []

        trigger_types = TriggerMaster.getTriggerTypes()
        liststore = gtk.ListStore(str, object)
        trigger_list = gtk.ComboBox(liststore)
        cellpb = gtk.CellRendererPixbuf()
	cell = gtk.CellRendererText()
        trigger_list.pack_start(cellpb, False)
        trigger_list.pack_start(cell, True)

	trigger_list.add_attribute(cell, 'text', 0)
        trigger_list.get_model().append(["Select a Trigger Type", None])
        
        for trigger_type in TriggerMaster.getTriggerTypes():
            trigger_list.get_model().append([trigger_type.__name__, trigger_type])

        trigger_list.set_active(0)
        trigger_list.connect("changed", self.trigger_type_changed)
        
        trigger_type = gtk.Label("Trigger Type:")
        trigger_type.show()
        trigger_list.show()

        self.trigger_list = trigger_list
        
        self.trigger_form = gtk.Table(rows=1, columns=2)    
        self.trigger_form.attach(trigger_type, 0, 1, 0, 1)
        self.trigger_form.attach(trigger_list, 1, 2, 0, 1)
        self.trigger_form.show()



        (label, input) = inpututils.Entry("Name").draw()
        self.trigger_name = input
        self.trigger_form.attach(label, 0, 1, 1, 2)
        self.trigger_form.attach(input, 1, 2, 1, 2)

        
        self.action_form = gtk.Table(rows=1, columns=2)
        self.action_form.show()
           
        add_action = gtk.Button("Add Another Action")
        add_action.show()

        add_action.connect("clicked", self.add_action)
        
        submit = gtk.Button("Save")
        submit.show()
        submit.connect("clicked", self.save_trigger)

        buttons = gtk.HBox()
        buttons.pack_start(add_action)
        buttons.pack_start(submit)
        buttons.show()
        
        form_holder = gtk.VBox()
        form_holder.pack_start(self.trigger_form, False)
        form_holder.pack_start(self.action_form, False)
        form_holder.pack_end(buttons, False)
        form_holder.show()

        self.add_action(None)

        return form_holder


    def set_view(self, view):
        """
        Set the current window to be the chosen window ''view''
        """
        
        print "Set view %s" % view
        
        if view == "summary":
            self.window.show()
        elif view == "new_trigger":
            if not hasattr(self, "trigger_view"):
                self.trigger_view = self.build_trigger_creation_window()
            self.trigger_view.show()

