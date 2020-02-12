from adjacent import Adjacent
from grid import Grid

class Dfs:

    def __init__(self, grid, s=0, adjacent=None):
        self.adj = adjacent
        if adjacent is None:
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
    grid = Grid()
    dfs = Dfs(grid.data)
    print("Bottom right corner is reachable: %s" % dfs.connected(len(grid.data)*len(grid.data[0])-1))
    grid.show()
