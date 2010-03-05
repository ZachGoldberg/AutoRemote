from gi.repository import GUPnP, GUPnPAV
import pygtk
pygtk.require('2.0')
import gtk, gobject, hildon

from controllers.TriggerMaster import TriggerMaster
from util import inputs as inpututils
from util.action import UPnPAction
from util.autoremotegui import AutoRemoteGUI

class HildonAutoRemoteGUI(AutoRemoteGUI):
    
    def __init__(self, upnp_backend):
        super(HildonAutoRemoteGUI, self).__init__(upnp_backend)
        
        self.window = hildon.StackableWindow()
        self.window.set_border_width(10)
        self.window.set_default_size(800,480)

        self.build_window_choser()

        self.set_view("summary")
        self.window.add(self.build_trigger_action_view())
        self.window.set_title("Auto Remote")
        self.window.show()


    def delete_trigger(self, button):
        self.remove_trigger(self.triggers[button.index[0]])

    def edit_trigger(self, button):
        super(HildonAutoRemoteGUI, self).edit_trigger(self.triggers[button.index[0]])
        
    def show_menu(self, treeview, index, column):
        menu = gtk.Menu()

        edit = gtk.MenuItem("Edit")
        delete = gtk.MenuItem("Delete")

        for button in [edit, delete]:
            button.treeview = treeview
            button.column = column
            button.index = index

        edit.connect("activate", self.edit_trigger)
        delete.connect("activate", self.delete_trigger)
        
        menu.add(edit)
        menu.add(delete)
        
        menu.show_all()
        menu.popup(None, None, None, 1, 0)

    def build_trigger_action_view(self):
        """
        Build a panel that will contain a list of all the
        already defined triggers in a HildonPannableView
        with a TreeView underneath        
        """
        self.item_list = super(HildonAutoRemoteGUI, self).build_trigger_action_view()

        self.item_list.connect("row-activated", self.show_menu)

        pannable = hildon.PannableArea()
        pannable.add(self.item_list)
        pannable.show()
       
        return pannable

    def build_window_choser(self):
        """
        Add a list of option to the ui toolbar which chose what view to be in        
        """

        summary_button = hildon.Button(0, 0, "Trigger List")
        summary_button.connect("clicked", lambda x, : self.set_view("summary"))

        new_button = hildon.Button(0, 0, "New Trigger")
        new_button.connect("clicked", lambda x, : self.set_view("new_trigger"))
        
        menu = hildon.AppMenu()
        menu.append(summary_button)
        menu.append(new_button)
        menu.show_all()

        self.window.set_app_menu(menu)
        

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

        area = hildon.PannableArea()
        area.add_with_viewport(self.action_form)
        area.show()        

        self.vbox = gtk.VBox()
        self.vbox.pack_start(self.trigger_form, False)
        self.vbox.pack_start(area)
        self.vbox.pack_end(buttons, False)
        self.vbox.show()

        form_holder = hildon.StackableWindow()
        form_holder.add(self.vbox)
        form_holder.show()
        
        if self.add_action_by_default:
            self.add_action(None)

        return form_holder


    def set_view(self, view):
        """
        Set the current window to be the chosen window ''view''
        """
        
        print "Hildon Set view %s" % view

        stack = hildon.WindowStack.get_default()

        if view == "summary":
            print self.window, self.window.get_title()            
            self.window.show_all()
            if stack.size() > 1:
                stack.pop(1)
            
        elif view == "new_trigger":
            self.trigger_view = self.build_trigger_creation_window()
            self.trigger_view.show()

