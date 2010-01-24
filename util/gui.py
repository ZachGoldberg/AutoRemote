#!/usr/bin/env python
from gi.repository import GUPnP, GUPnPAV
import pygtk
pygtk.require('2.0')
import gtk, gobject

from controllers.TriggerMaster import TriggerMaster
from util import inputs as inpututils

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
        print trigger
        self.item_list.get_model().append([trigger.name])
 
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

    def source_changed(self, box):
        print box
        trigger_class = box.get_model().get_value(box.get_active_iter(), 1)
        inputs = [inpututils.Entry("Name")]
        inputs.extend(trigger_class.get_editable_fields())
                                        
        cur_row = 1
        for input in inputs:
            (label, input) = input.draw()
            self.trigger_form.attach(label, 0, 1, cur_row, cur_row + 1)
            self.trigger_form.attach(input, 1, 2, cur_row, cur_row + 1)
            cur_row += 1


    def add_action(self, button):
        print "Add Action"
        renderers = [(n.get_friendly_name(), n) for n in self.upnp.renderers]
        action_inputs = [
            inpututils.Entry("Name"),        
            inpututils.Selection("Target Renderer", renderers, False),
            ]

        self.render_lists.append(action_inputs[1].draw()[1])

        cur_row = self.action_form.get_property("n_rows")
        for input in action_inputs:
            (label, input) = input.draw()
            print label
            self.action_form.attach(label, 0, 1, cur_row, cur_row + 1)
            self.action_form.attach(input, 1, 2, cur_row, cur_row + 1)
            cur_row += 1

        
    def build_gtk_trigger_creation_window(self, button=None):
        self.summary_window.hide()
        
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
        trigger_list.connect("changed", self.source_changed)
        
        trigger_type = gtk.Label("Trigger Type:")
        trigger_type.show()
        trigger_list.show()
        self.trigger_form = gtk.Table(rows=1, columns=2)    
        self.trigger_form.attach(trigger_type, 0, 1, 0, 1)
        self.trigger_form.attach(trigger_list, 1, 2, 0, 1)
        self.trigger_form.show()
        
        self.action_form = gtk.Table(rows=1, columns=2)
        self.action_form.show()

        for i in self.window.get_children():
            self.window.remove(i)


        add_action = gtk.Button("Add Another Action")
        add_action.show()

        add_action.connect("clicked", self.add_action)
        
        submit = gtk.Button("Save")
        submit.show()

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

        self.window.add(form_holder)


    def build_gtk_window_choser(self):
        if hasattr(self, "window_choser"):
            return self.window_choser
        
        self.window_choser = gtk.HBox()
        
        self.summary_button = gtk.Button("Summary")
        self.new_trigger_button = gtk.Button("New Trigger")

        self.new_trigger_button.connect("clicked", self.build_gtk_trigger_creation_window)

        self.window_choser.pack_start(self.summary_button)
        self.window_choser.pack_start(self.new_trigger_button)


        self.summary_button.show()
        self.new_trigger_button.show()

        self.window_choser.show()

        return self.window_choser
            

    def build_trigger_action_view(self):
        tree_model = gtk.ListStore(str)
        self.trigger_action_view = gtk.TreeView(tree_model)
        
        col = gtk.TreeViewColumn("Triggers")
        col.cell = gtk.CellRendererText()
        col.pack_start(col.cell)
        col.set_attributes(col.cell, text=0)
        self.trigger_action_view.append_column(col)
        #self.trigger_action_view.connect("row-activated", self.enqueue_or_dive)

        self.trigger_action_view.show()
        return self.trigger_action_view

    def build_gtk_summary_window(self):
        #----- GTK Version (includes buttons and a GTKTreeView)
        self.summary_window = gtk.VBox() 
        self.window_list = self.build_gtk_window_choser()
        

        self.item_list = self.build_trigger_action_view()

        self.summary_window.pack_start(self.window_list, False)
        self.summary_window.add(self.item_list)
        self.summary_window.show()        

        self.window.add(self.summary_window)


    def set_view(self, view):
        if view == "new_trigger":
            self.build_gtk_trigger_creation_window()
        elif view == "summary":
            self.build_gtk_summary_window()

    def __init__(self, upnp_backend):
        self.upnp = upnp_backend

        self.sources = []
        self.icons = {}
        self.renderers = []
        self.items = []
        self.stack = []

        self.render_lists = []
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)
        self.window.set_default_size(800,480)

        self.set_view("summary")
        self.set_view("new_trigger")        
        self.window.show()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    hello = HelloWorld()
    hello.main()
