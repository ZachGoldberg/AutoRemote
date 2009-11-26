#!/usr/bin/env python
from gi.repository import GUPnPAV
import pygtk
pygtk.require('2.0')
import gtk, gobject

class PyGUPnPCPUI(object):
    def hello(self, widget, data=None):
        print "Hello World"

    def delete_event(self, widget, event, data=None):
        print "delete event occurred"
        return False

    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit()

    def source_changed(self, box):
        print "Source Changed"
        active = self.source_list.get_active()
        if active == 0: # The title entry
            return
        active -= 1

        self.stack = []
        self.source_device = self.sources[active]
        self.upnp.load_children(self.source_device)

    def renderer_changed(self, box):
        print "Renderer Changed"
        active = self.renderer_list.get_active()
        if active == 0: # The title entry
            return
        active -= 1

        self.renderer_device = self.renderers[active]

    def play_or_dive(self, tree, col_loc, col):
        print "Row activated"
        item = self.items[col_loc[0]]
        if isinstance(item, GUPnPAV.GUPnPDIDLLiteContainer):
            self.stack.append(item.get_parent_id())
            self.upnp.load_children(self.source_device, item.get_id())
        elif isinstance(item, GUPnPAV.GUPnPDIDLLiteItem):
            print "Begin playing %s" % item.get_title()
            self.upnp.play_object(self.source_device,
                                  self.renderer_device,
                                  item)
        else:
            if len(self.stack) > 0:
                self.upnp.load_children(self.source_device, 
                                        self.stack.pop())
            
    def add_source_item(self, item, txt):
        self.items.append(item)
        self.source_browser.get_model().append([txt])

    def clear_source_browser(self):
        self.source_browser.get_model().clear()
        self.items = []
        self.add_source_item(None, "..")
        
    def add_container(self, container):
        self.add_source_item(container, "(+) %s" % container.get_title())

    def add_object(self, object):
        self.add_source_item(object, object.get_title())
        
    def add_renderer(self, device):
        self.renderer_list.append_text(device.get_model_name())
        self.renderers.append(device)
        if len(self.renderers) == 1:
            self.renderer_list.set_active(1)

    def add_source(self, device):
        self.source_list.append_text(device.get_model_name())
        self.sources.append(device)
        if len(self.sources) == 1:
            self.source_list.set_active(1)
            
            
    def init_top_bar(self):
        self.top_bar = gtk.HBox()
	
        self.source_list = gtk.combo_box_new_text()
	self.source_list.insert_text(0, "Media Sources")
        self.source_list.set_active(0)
        self.source_list.connect("changed", self.source_changed)

        self.renderer_list = gtk.combo_box_new_text()
	self.renderer_list.insert_text(0, "Media Players")
        self.renderer_list.set_active(0)        
        self.renderer_list.connect("changed", self.renderer_changed)

        self.top_bar.pack_start(self.source_list)
        self.top_bar.pack_start(self.renderer_list)
        self.source_list.show()
        self.renderer_list.show()
        self.top_bar.show()

        return self.top_bar

    def init_main_bar(self):
        self.main_bar = gtk.HBox(homogeneous=True)
        
        tree_model = gtk.ListStore(str)
        self.source_browser = gtk.TreeView(tree_model)
        col = gtk.TreeViewColumn("Media Items in this Source")
        col.cell = gtk.CellRendererText()
        col.pack_start(col.cell)
        col.set_attributes(col.cell, text=0)
        self.source_browser.append_column(col)
        self.source_browser.connect("row-activated", self.play_or_dive)

        self.player = gtk.VBox()
        self.play_button = gtk.Button("Play")
        self.player.pack_start(self.play_button, False)
        self.play_button.show()

        self.main_bar.pack_start(self.source_browser)
        self.main_bar.pack_start(self.player)
        self.main_bar.show()
        self.source_browser.show()
        self.player.show()

        return self.main_bar

    def __init__(self, upnp_backend):
        self.upnp = upnp_backend

        self.sources = []
        self.renderers = []
        self.items = []
        self.source_device = None
        self.stack = []
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)
        self.window.set_default_size(800,480)

        self.vbox = gtk.VBox(homogeneous=False)

        self.vbox.pack_start(self.init_top_bar(), False)
        self.vbox.pack_start(self.init_main_bar(), True)
        self.window.add(self.vbox)
        self.window.show()
        self.vbox.show()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    hello = HelloWorld()
    hello.main()
