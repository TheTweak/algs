from appJar import gui

def generategrid(w=16, h=16):
    rows = []
    for x in range(w):
        row = [0 for _ in range(h)]
        rows.append(row)            
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

if __name__ == "__main__":
    grid = generategrid()
    showgrid(grid)
