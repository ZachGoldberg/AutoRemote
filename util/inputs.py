import gtk

class Input(object):
    def __init__(self, label, userdata=None):
        self.label = label
        self.obj = None
        self.gtk_label = None
        self.userdata = userdata


    def get_userdata(self):
        return self.userdata
    
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

    def get_value(self):
        raise "Unimplemented!"
    
    def set_value(self):
        raise "Unimplemented!"

class Selection(Input):
    def __init__(self, label, options, userdata=None, string_only=True):
        super(Selection, self).__init__(label, userdata)
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
        self.list_input = list_input
        return list_input

    def get_value(self):
        iter = self.list_input.get_active_iter()
        if not iter:
            return None
        
        if self.string_only:
            return self.list_input.get_model().get_value(iter, 0)
        else:
            return [
                self.list_input.get_model().get_value(iter, 0),
                self.list_input.get_model().get_value(iter, 1)
                ]

    def set_value(self, value, index=0, func=None):
        model = self.list_input.get_model()
        iterv = model.get_iter_first()
        count = model.iter_n_children(None)

        for i in range(0, count):
            if not func:
                if model.get_value(iterv, index) == value:
                    self.list_input.set_active(i)
                    return True
            else:
                if func(model.get_value(iterv, index)) == value:
                    self.list_input.set_active(i)
                    return True
                
            iterv = model.iter_next(iterv)            
 
        return False
    
class Entry(Input):
    def __init__(self, label, userdata=None):
        super(Entry, self).__init__(label, userdata)


    def draw_input(self):        
        self.entry = gtk.Entry()
        self.entry.show()
        return self.entry

    def get_value(self):
        return self.entry.get_text()

    def set_value(self, text):
        self.entry.set_text(text)
