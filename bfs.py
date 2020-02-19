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
            if not self.visited[v]:
                for a in adjacent.get(v):
                    if not self.visited[a]:
                        self.edge_to[a] = v
                        queue.append(a)
            self.visited[v] = True

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
    parser.add_argument("-size", default=16, help="Grid size", type=int)
    parser.add_argument("-bs", default=3, help="Grid obstacle block size", type=int)
    args = parser.parse_args()
    s = time.time()
    grid = Grid(w=args.size, h=args.size, block_size=args.bs)
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
        grid.set_cell_color(v=v, color=[255, 255, 0])
    grid.show()
