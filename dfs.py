from appJar import gui
import random

class Adjacent:

    def __init__(self, grid):
        self.adj = []
        self.w = len(grid[0])
        self.h = len(grid)
        for r, row in enumerate(grid):
            for c, col in enumerate(row):
                adjacent = []
                if r-1 >= 0 and grid[r-1][c] == 0:
                    adjacent.append(c+len(row)*(r-1))
                if r+1 < len(grid) and grid[r+1][c] == 0:
                    adjacent.append(c+len(row)*(r+1))
                if c-1 >= 0 and grid[r][c-1] == 0:
                    adjacent.append(c-1+len(row)*r)
                if c+1 < len(row) and grid[r][c+1] == 0:
                    adjacent.append(c+1+len(row)*r)
                self.adj.append(adjacent)

    def get(self, r, c=None):
        n = r
        if c is not None:
            n = c + self.w*r
        return self.adj[n]

class Dfs:

    def __init__(self, grid, s=0):
        self.adj = Adjacent(grid)
        self.visited = [0 for _ in range(len(grid)*len(grid[0]))]
        self.edge_to = [0 for _ in range(len(grid)*len(grid[0]))]
        stack = []
        stack.append(s)
        while True:
            try:
                v = stack.pop()
            except IndexError:
                v = None
            if v is None:
                break
            if not self.visited[v]:
                self.visited[v] = True
                for a in self.adj.get(v):
                    self.edge_to[a] = v
                    stack.append(a)

    def connected(self, d):
        return self.visited[d]

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

if __name__ == "__main__":
    grid = generategrid()
    adj = Adjacent(grid)
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            print("Adjacent Vs for (%s, %s): %s" % (r, c, adj.get(r, c)))
    dfs = Dfs(grid)
    print("Bottom right corner is reachable: %s" % dfs.connected(len(grid)*len(grid[0])-1))
    showgrid(grid)
