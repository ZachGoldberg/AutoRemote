import gtk

class Input(object):
    def __init__(self, label):
        self.label = label

    def getLabel(self):
        return self.label

    def draw(self):
        
        label = gtk.Label(self.label)
        label.show()
        
        return (label, self.draw_input())

    def draw_input(self):
        print "Called Super"
        raise "Unimplemented!"
    
class Selection(Input):
    def __init__(self, label, options):
        super(Selection, self).__init__(label)
        self.options = options


    def draw_input(self):
        liststore = gtk.ListStore(str)
        for opt in self.options:
            liststore.append([opt])

        list_input = gtk.ComboBox(liststore)
	cell = gtk.CellRendererText()
        list_input.pack_start(cell, True)
	list_input.add_attribute(cell, 'text', 0)


        list_input.set_active(0)
        list_input.show()
        return list_input
