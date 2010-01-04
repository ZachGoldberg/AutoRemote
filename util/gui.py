#!/usr/bin/env python
from gi.repository import GUPnP, GUPnPAV
import pygtk
pygtk.require('2.0')
import gtk, gobject


class AutoRemoteUI(object):
    def delete_event(self, widget, event, data=None):
        print "delete event occurred"
        return False

    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit()

    def add_renderer(self, device, icon_file):
        self.icons[device.get_udn()] = icon_file
        self.renderer_list.get_model().append([device.get_model_name(), gtk.STOCK_OPEN, device])
        self.renderers.append(device)
        if len(self.renderers) == 1:
            self.renderer_list.set_active(1)

    def add_source(self, device, icon_file):
        self.icons[device.get_udn()] = icon_file
        self.source_list.get_model().append([device.get_friendly_name(), gtk.STOCK_OPEN, device])
        
        self.sources.append(device)
        if len(self.sources) == 1:
            self.source_list.set_active(1)
    
    def remove_renderer(self, device):
        self.remove_device(device, self.renderers, self.renderer_device, self.renderer_list)
        
    def remove_source(self, device):
        self.remove_device(device, self.sources, self.source_device, self.source_list)
      

    def remove_device(self, device, cache_list, cache_item, ui_list):
        for d in cache_list:
            if d.get_udn() == device.get_udn():
                cache_list.remove(d)
                if d.get_udn() == cache_item.get_udn():
                    if len(cache_list) > 1:
                        ui_list.set_active(1)
                    else:
                        ui_list.set_active(0)

        model = ui_list.get_model()
        iter =  model.get_iter(0)
        while iter and model.iter_is_valid(iter):
            iter = model.iter_next(iter)
            if iter and model.get_value(iter, 2).get_udn() == device.get_udn():
                model.remove(iter)

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


    def build_gtk_window_choser(self):
        if hasattr(self, "window_choser"):
            return self.window_choser
        
        self.window_choser = gtk.HBox()
        
        self.summary_button = gtk.Button("Summary")
        self.new_trigger_button = gtk.Button("New Trigger")
        self.new_action_button  = gtk.Button("New Action")

        self.window_choser.pack_start(self.summary_button)
        self.window_choser.pack_start(self.new_trigger_button)
        self.window_choser.pack_start(self.new_action_button)


        self.summary_button.show()
        self.new_trigger_button.show()
        self.new_action_button.show()

        self.window_choser.show()

        return self.window_choser
            

    def build_gtk_summary_window(self):
        #----- GTK Version (includes buttons and a GTKTreeView
        self.summary_box = gtk.VBox() 
        self.window_list = self.build_gtk_window_choser()
        self.summary_box.add(self.window_list)
        self.summary_box.show()

        return self.summary_box

    def __init__(self, upnp_backend):
        self.upnp = upnp_backend

        self.sources = []
        self.icons = {}
        self.renderers = []
        self.items = []
        self.stack = []
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)
        self.window.set_default_size(800,480)
        self.window.add(self.build_gtk_summary_window())
        self.window.show()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    hello = HelloWorld()
    hello.main()
