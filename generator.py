import os
import random

import drawsvg as draw
import numpy as np

import db
import geom as g

max_components = 10
num_designs = 3
component_ds = 32
pin_ds = 8


def row_col_from_index(index, dx, dy):
    row = index // dx
    col = index % dx

    return row, col


def create_basic_macro(a_db):
    w = component_ds
    h = component_ds

    pin_rect = g.Rect(g.XY(-pin_ds / 2, -pin_ds / 2), g.XY(pin_ds / 2, pin_ds / 2))

    pins = list()
    pins.append(db.Pin("N", pin_rect.move_by(w / 2, h)))
    pins.append(db.Pin("E", pin_rect.move_by(w, h / 2)))
    pins.append(db.Pin("S", pin_rect.move_by(w / 2, 0)))
    pins.append(db.Pin("W", pin_rect.move_by(0, h / 2)))
    macro = db.Macro("cell", None, g.Rect(g.XY(0, 0), g.XY(w, h)), pins)
    a_db.add_macro(macro)

    return macro


def create_db(world_bounds):
    # Create Top Level Macro
    newdb = db.DB("db")
    design = db.Macro("Design", None, world_bounds, None)
    newdb.add_macro(design)
    newdb.set_top_macro(design)

    return newdb


def create_cell(newdb):
    cell = create_basic_macro(newdb)

    return cell


def draw_geometry(display, r, color):
    outline = draw.Rectangle(r.ll.x, r.ll.y, r.width(), r.height(), fill=color)
    display.append(outline)


def draw_component(display, component):
    r = component.macro.rect.move_by(component.loc.x, component.loc.y)
    draw_geometry(display, r, "white")
    for p in component.macro.pins:
        r = p.rect.move_by(component.loc.x, component.loc.y)
        draw_geometry(display, r, "red")


def draw_net(display, db):
    for c in db.connections:
        l = draw.Line(c.line.xy[0][0], c.line.xy[0][1], c.line.xy[1][0], c.line.xy[1][1], stroke='black',
                      stroke_width=1)
        display.append(l)


def draw_db(display, db):
    r = db.die.rect
    outline = draw.Rectangle(r.ll.x, r.ll.y, r.width(), r.height(), fill='green')
    display.append(outline)
    for c in db.devices:
        draw_component(display, c)
    draw_net(display, db)


def create_connections(a_db):
    die = a_db.die
    for n in die.nets:
        pin_list = list()
        for c in die.children:
            for net_on_component in c.parent_net_map:
                if n == net_on_component:
                    pin = c.parent_net_map.get(net_on_component)
                    pin_list.append((c, pin))
        for pin_idx in range(len(pin_list) - 1):
            from_pin = pin_list[pin_idx]
            to_pin = pin_list[pin_idx + 1]

            connection = db.Connection(from_pin[0], to_pin[0], from_pin[1], to_pin[1])
            a_db.add_connection(connection)


def lattice_generator():
    num_columns = random.randint(1, max_components)
    num_rows = random.randint(1, max_components)

    # draw the design bounds
    num_components = num_columns * num_rows
    max_x = (num_columns * component_ds * 2) + component_ds
    max_y = (num_rows * component_ds * 2) + component_ds
    seq = np.random.permutation(num_components)
    drawing = draw.Drawing(max_x, max_y)
    ll = g.XY(0, 0)
    ur = g.XY(max_x, max_y)

    world_bounds = g.Rect(ll, ur)
    new_db = create_db(world_bounds)
    cell = create_cell(new_db)
    parent = new_db.die

    component_array = np.full((num_components), None)

    # draw the devices
    for idx in range(num_components):
        component_idx = seq[idx]
        row, col = row_col_from_index(component_idx, num_columns, num_rows)
        x = col * (component_ds * 2) + component_ds
        y = row * (component_ds * 2) + component_ds
        name = "cell(" + str(x) + "," + str(y) + ")"
        component = db.Component(name, cell, g.XY(x, y), parent)
        new_db.add_device(component)
        component_array[idx] = component

    # create nets

    net_num = 0
    for idx in range(num_components - 2):
        row, col = row_col_from_index(idx, num_columns, num_rows)
        this_component = component_array[idx]
        if col == num_columns - 1:
            right_component = None
        else:
            right_component = component_array[idx + 1]
        if row == num_rows - 1:
            above_component = None
        else:
            above_component = component_array[idx + num_columns]

        # set the nets between adjacent pins
        if right_component != None:
            from_pin = this_component.macro.get_pin_by_name("E")
            to_pin = right_component.macro.get_pin_by_name("W")
            net = db.Net("net-" + str(net_num), this_component.parent)
            this_component.set_net(from_pin, net)
            right_component.set_net(to_pin, net)
        if above_component != None:
            from_pin = this_component.macro.get_pin_by_name("N")
            to_pin = above_component.macro.get_pin_by_name("S")
            net = db.Net("net-" + str(net_num), this_component.parent)
            this_component.set_net(from_pin, net)
            above_component.set_net(to_pin, net)

    create_connections(new_db)

    return new_db, drawing


class Label:
    def __init__(self, file: chr, score: float):
        self.filename = file
        self.score = score


def create_lines(a_db):
    l = list()
    for c in a_db.connections:
        l.append(c.line)
    return l


def determine_score(a_db):
    total, crosses = g.det_crosses(create_lines(a_db))
    score = crosses / total
    return score


def create_label_files(labels):
    os.chdir("..")
    f = open("labels.csv", "w")

    for label in labels:
        s = label.filename + "," + str(label.score) + '\n'
        f.write(s)
    f.close()


def create_test_cases():
    labels = list()
    os.chdir("generated_images")
    for design_idx in range(num_designs):
        a_db, drawing = lattice_generator()
        filename = 't' + str(design_idx) + '.svg'
        draw_db(drawing, a_db)
        drawing.save_svg(filename)
        score = determine_score(a_db)
        labels.append(Label(filename, score))

    create_label_files(labels)


create_test_cases()
