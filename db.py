# in the spirit of lef/def and verilog
# https://coriolis.lip6.fr/doc/lefdef/lefdefref/lefdefref.pdf


class DB:
    def __init__(self, name):
        self.name = name
        self.macros = list()
        self.devices = list()
        self.top_macro = None

    def set_top_macro(self, macro):
        self.top_macro = macro

    def add_macro(self, macro):
        self.macros.append(macro)

    def add_device(self, device):
        self.devices.append(device)


class Net:
    def __init__(self, name, macro):
        self.name = name
        macro.nets.append(self)


class Pin:
    def __init__(self, name, rect):
        self.name = name
        self.rect = rect

class Macro:
    def __init__(self, name, children, rect, pins):
        self.children = list()
        self.name = name
        self.rect = rect
        self.pins = pins
        self.nets = None
        self.nets = list()


    def add_child(self, child):
        self.children.add(child)

    def get_pin_by_name (self, name):
        for p in self.pins:
            if p.name == name:
                return p
        return None



class Component:
    def __init__(self, name, macro, loc, parent):
        self.name = name
        self.macro = macro
        self.loc = loc
        self.parent = parent
        parent.children.append(self)
        self.parent_net_map = {}

    def set_net (self, template_pin, net):
        self.parent_net_map.update ({net:template_pin})




