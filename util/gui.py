#!/usr/bin/env python
from gi.repository import GUPnP, GUPnPAV
import pygtk
pygtk.require('2.0')
import gtk, gobject

from controllers.TriggerMaster import TriggerMaster
from util import inputs as inpututils
from util.action import UPnPAction

class AutoRemoteUI(object):
    def delete_event(self, widget, event, data=None):
        print "delete event occurred"
        return False

    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit()

    def add_renderer(self, device):
        for rlist in self.render_lists:
            rlist.get_model().append([device.get_friendly_name(), device])
            count = rlist.get_model().iter_n_children(None)
            if count == 1:
                rlist.set_active(0)

    def remove_renderer(self, device):
        for rlist in self.render_lists:
            model = rlist.get_model()            
            count = rlist.get_model().iter_n_children(None)
            iterv = model.get_iter_first()
            for i in range(0, count):
                if model.get_value(iterv, 1).get_udn() == device.get_udn():

                    # If we're removing the active element then reset active to 0th element
                    if str(rlist.get_active()) == model.get_string_from_iter(iterv):
                        rlist.set_active(0)
                        
                    model.remove(iterv)                    
                    break
                
                iterv = model.iter_next(iterv)
                
            
    def add_trigger(self, trigger):
        self.item_list.get_model().append([trigger.get_name()])
 
    def make_pb(self, col, cell, model, iter):
        stock = model.get_value(iter, 1)
	if not stock:
	    return

        device = model.get_value(iter, 2)

        if device and self.icons[device.get_udn()]:
            pb = gtk.gdk.pixbuf_new_from_file(self.icons[device.get_udn()])
            pb = pb.scale_simple(22, 22, gtk.gdk.INTERP_HYPER)
        else:
            pb = self.source_list.render_icon(stock, gtk.ICON_SIZE_MENU, None)

        cell.set_property('pixbuf', pb)
        return

    def trigger_type_changed(self, box):
        print box
        trigger_class = box.get_model().get_value(box.get_active_iter(), 1)
        inputs = trigger_class.get_editable_fields()
        self.current_editables = inputs
        cur_row = 2
        for input in inputs:
            (label, input) = input.draw()
            self.trigger_form.attach(label, 0, 1, cur_row, cur_row + 1)
            self.trigger_form.attach(input, 1, 2, cur_row, cur_row + 1)
            cur_row += 1


    def save_trigger(self, button):
        print "Save!"
        trig_type = self.trigger_list.get_model().get_value(
            self.trigger_list.get_active_iter(), 1)
        if not trig_type:
            return

        trig_name = self.trigger_name.get_text()
        print trig_type, trig_name
        
        for v in self.current_editables:
            print v.get_value()

        for a in self.actions:
            for i in a:
                print i.get_value()
                
        # First build a list of actions chained together,
        # then build a trigger containing that action
        action = None
        last_action = None
        for a in self.actions:
            device = a[0].get_value()[1]
            data = a[1].get_value()
            service = self.upnp.get_service_on_device(device, "AVTransport")
            act = UPnPAction(device, service, data, None)
            if not action:
                action = act
                last_action = act
            else:
                last_action.next_action = act

            last_action = act

        triggerdata = {}
        for v in self.current_editables:
            triggerdata[v.get_userdata()] = v.get_value()

        triggerdata["upnpaction"] = action
        triggerdata["trigger_class"] = trig_type.__name__
        trigger = trig_type(triggerdata)
        trigger.name = trig_name


        self.remote.add_trigger(trigger)
        self.add_trigger(trigger)
        
        self.set_view("summary")

    def add_action(self, button):
        print "Add Action"
        renderers = [(n.get_friendly_name(), n) for n in self.upnp.renderers]
        renderer_actions = ["Stop", "Pause", "Play", "Next", "Prev"]
        action_inputs = [
            inpututils.Selection("Target Renderer", renderers, string_only=False),
            inpututils.Selection("Action", renderer_actions, string_only=True)
            ]

        self.actions.append(action_inputs)
        self.render_lists.append(action_inputs[0].draw()[1])

        cur_row = self.action_form.get_property("n_rows")
        for input in action_inputs:
            (label, input) = input.draw()
            print label
            self.action_form.attach(label, 0, 1, cur_row, cur_row + 1)
            self.action_form.attach(input, 1, 2, cur_row, cur_row + 1)
            cur_row += 1

        
    def build_trigger_creation_window(self, button=None):
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


    def build_window_choser(self):
        window_choser = gtk.HBox()
        
        summary_button = gtk.Button("Summary")
        new_trigger_button = gtk.Button("New Trigger")

        summary_button.loc = "summary"
        new_trigger_button.loc = "new_trigger"

        summary_button.connect("clicked", self.set_view_button)
        new_trigger_button.connect("clicked", self.set_view_button)

        window_choser.pack_start(summary_button)
        window_choser.pack_start(new_trigger_button)


        summary_button.show()
        new_trigger_button.show()

        window_choser.show()

        return window_choser
            

    def build_trigger_action_view(self):
        tree_model = gtk.ListStore(str)
        self.trigger_action_view = gtk.TreeView(tree_model)
        
        col = gtk.TreeViewColumn("Triggers")
        col.cell = gtk.CellRendererText()
        col.pack_start(col.cell)
        col.set_attributes(col.cell, text=0)
        self.trigger_action_view.append_column(col)
        self.trigger_action_view.show()

        return self.trigger_action_view

    def build_summary_window(self):
        if not hasattr(self, "item_list"):
            print "Begin"
            self.item_list = self.build_trigger_action_view()
            print "End"

        return self.item_list


    def set_view_button(self, button):
        self.set_view(button.loc)
        
    def set_view(self, view):
        # Clear the window first
        for c in self.window.get_children():
            self.window.remove(c)

        if hasattr(self, "item_list"):
            print self.item_list.get_model() , "MODEL2"

        print "Set view %s" % view

        if hasattr(self, "summary_window"):
            for c in self.summary_window.get_children():
                self.summary_window.remove(c)

        self.summary_window = gtk.VBox()
        self.window_list = self.build_window_choser()

        self.trigger_view = self.build_trigger_creation_window()
        self.summary_view = self.build_summary_window()
        
        if view == "new_trigger":
            content = self.trigger_view    
        if view == "summary":
            content = self.summary_view

        content.show()

        self.summary_window.pack_start(self.window_list, False)
        self.summary_window.add(content)
        self.summary_window.show()        
        self.window.add(self.summary_window)

    def __init__(self, upnp_backend):
        self.upnp = upnp_backend

        self.sources = []
        self.icons = {}
        self.renderers = []
        self.items = []
        self.stack = []
        self.render_lists = []
        
