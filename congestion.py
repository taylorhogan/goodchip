import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np
import shapely
import generator
import config

# TODO this is a work in progress.
def fun (x, y):
    z = np.array
    for row in x:
        for col in y:
            return 1





def inject_c_in_congestion (z, l, r, rows, cols, dx, dy):
    for row_idx in range(rows):
        bot = row_idx*dy
        for col_idx in range(cols):
            left = col_idx*dx
            box = shapely.box (left, bot, left+dx, bot+dy)
            if shapely.intersects(l,box):
                z[row_idx][col_idx]= z[row_idx][col_idx] +1




def determine_congestion (a_db):
    cfg = config.Config ()
    ds = cfg.get_pin_ds()
    box = a_db.die.rect.to_shapely_box()
    rows = round(a_db.die.rect.width() / ds);
    cols = round(a_db.die.rect.height() / ds);
    z = np.zeros(shape = (rows, cols), dtype=np.float64)

    for c in a_db.connections:
        inject_c_in_congestion(z, c.line, box, rows, cols, ds, ds)
    return z





a_db, drawing = generator.lattice_generator(1)
z = determine_congestion(a_db)
generator.draw_db(drawing, a_db)
drawing.save_svg("foo.svg")
print (z)



