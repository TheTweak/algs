from adjacent import Adjacent
import copy
from grid import Grid

class Bfs:

    def __init__(self, grid, s=0):
        self.s = s
        adj = Adjacent(grid)
        self.visited = [0 for _ in range(len(grid)*len(grid[0]))]
        self.edge_to = [-1 for _ in range(len(grid)*len(grid[0]))]
        queue = []
        queue.append(s)
        while len(queue) != 0:
            v = queue.pop(0)
            self.visited[v] = True
            for a in adj.get(v):
                if not self.visited[a]:
                    self.edge_to[a] = v
                    queue.append(a)

    def shortest_path(self, d):
        path = [d]
        v = d
        while True:
            if v == self.s:
                break
            edge_to_v = self.edge_to[v]
            path.append(edge_to_v)
            v = edge_to_v
        path.reverse()
        return path

if __name__ == "__main__":
    grid = Grid()
    adj = Adjacent(grid.data)
    bfs = Bfs(grid.data)
    print("Shortest path to bottom right: %s" % bfs.shortest_path(len(grid.data)*len(grid.data[0])-1))
    grid.show()
