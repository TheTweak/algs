from appJar import gui
import random

def generategrid(w=5, h=5):
    rows = []
    for x in range(w):
        row = [0 if random.random() > 0.2 else 1 for _ in range(h)]
        rows.append(row)            
    # top left and bottom right is always 0
    rows[0][0] = 0
    rows[len(rows)-1][len(rows)-1] = 0
    return rows

def showgrid(grid):
    app=gui("Grid Demo", "300x300")
    
    app.setSticky("news")
    app.setExpand("both")
    app.setFont(20)
    
    for x, r in enumerate(grid):
        for y, c in enumerate(r):
            l = "l-%s-%s" % (x, y)
            lb = app.addLabel(l, "", x, y)
            app.setLabelBg(l, "Green" if c == 0 else "Black")
            app.setLabelRelief(l, "sunken")

    app.go()

