from adjacent import Adjacent
import copy
from grid import Grid
from dfs import Dfs
import argparse

class Bfs:

    def __init__(self, grid, s=0, adjacent=None):
        self.s = s
        if adjacent is None:
            adjacent = Adjacent(grid)
        self.visited = [0 for _ in range(len(grid)*len(grid[0]))]
        self.edge_to = [-1 for _ in range(len(grid)*len(grid[0]))]
        queue = []
        queue.append(s)
        while len(queue) != 0:
            v = queue.pop(0)
            self.visited[v] = True
            for a in adjacent.get(v):
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
    import time
    parser = argparse.ArgumentParser()
    parser.add_argument("-width", default=16, help="Grid width")
    parser.add_argument("-height", default=16, help="Grid height")
    args = parser.parse_args()
    s = time.time()
    grid = Grid(w=args.width, h=args.height)
    print("Grid creation: %s s" % (time.time() - s))
    s = time.time()
    adjacent = Adjacent(grid.data)
    print("Adjacent structure: %s s" % (time.time() - s))
    s = time.time()
    dfs = Dfs(grid.data, adjacent=adjacent)
    print("Dfs: %s s" % (time.time() - s))
    bottom_right = len(grid.data)*len(grid.data[0])-1
    if not dfs.connected(bottom_right):
        print("Bottom right corner is not reachable")
        exit(1)
    s = time.time()
    bfs = Bfs(grid.data, adjacent=adjacent)
    shortest_path = bfs.shortest_path(bottom_right)
    print("Shortest path: %s s" % (time.time() - s))
    for v in shortest_path:
        grid.set_cell_color(v=v, color=[127, 127, 127])
    grid.show()