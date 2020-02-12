from appJar import gui
import random

class Grid:

    def __init__(self, w=5, h=5):
        self.h = h
        self.w = w
        self.app=gui("Grid Demo", "300x300")
        
        self.app.setSticky("news")
        self.app.setExpand("both")
        self.app.setFont(20)
        self.data = self.generategrid(w=w, h=h)
        for x, r in enumerate(self.data):
            for y, c in enumerate(r):
                l = "l-%s-%s" % (x, y)
                lb = self.app.addLabel(l, "", x, y)
                self.app.setLabelBg(l, "Green" if c == 0 else "Black")
                self.app.setLabelRelief(l, "sunken")

    def generategrid(self, w=5, h=5):
        rows = []
        for x in range(w):
            row = [0 if random.random() > 0.2 else 1 for _ in range(h)]
            rows.append(row)            
        # top left and bottom right is always 0
        rows[0][0] = 0
        rows[len(rows)-1][len(rows)-1] = 0
        return rows

    '''
    Change color of cell V (sequential number)
    '''
    def set_cell_color(self, *, v, color):
        x = int(v / self.w)
        y = v - x * self.w
        print("cell# %s is (%s, %s)" % (v, x, y))
        self.app.setLabelBg("l-%s-%s" % (x, y), color)

    def show(self):
        self.app.go()

