import gtk

class Input(object):
    def __init__(self, label):
        self.label = label
        self.obj = None
        self.gtk_label = None
        
    def getLabel(self):
        return self.label

    def draw(self):
        if not self.gtk_label:    
            self.gtk_label = gtk.Label(self.label)
            self.gtk_label.show()

        if not self.obj:
            self.obj = self.draw_input()
            self.obj.show()
            
        return (self.gtk_label, self.obj)
        
    def draw_input(self):
        print "Called Super"
        raise "Unimplemented!"
    
class Selection(Input):
    def __init__(self, label, options, string_only=True):
        super(Selection, self).__init__(label)
        self.options = options
        self.string_only = string_only

    def draw_input(self):        
        if self.string_only:
            liststore = gtk.ListStore(str)
        else:
            liststore = gtk.ListStore(str, object)
                
        for opt in self.options:
            if isinstance(opt, (list, tuple)):
                liststore.append(opt)
            else:
                liststore.append([opt])
                    
        list_input = gtk.ComboBox(liststore)
	cell = gtk.CellRendererText()
        list_input.pack_start(cell, True)
	list_input.add_attribute(cell, 'text', 0)


        list_input.set_active(0)
        list_input.show()
        return list_input

class Entry(Input):
    def __init__(self, label):
        super(Entry, self).__init__(label)


    def draw_input(self):        
        self.entry = gtk.Entry()
        self.entry.show()
        return self.entry
