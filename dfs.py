from adjacent import Adjacent
from grid import (
        generategrid,
        showgrid
    )

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

if __name__ == "__main__":
    grid = generategrid()
    adj = Adjacent(grid)
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            print("Adjacent Vs for (%s, %s): %s" % (r, c, adj.get(r, c)))
    dfs = Dfs(grid)
    print("Bottom right corner is reachable: %s" % dfs.connected(len(grid)*len(grid[0])-1))
    showgrid(grid)
