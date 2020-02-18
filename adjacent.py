class Adjacent:

    def __init__(self, grid):
        self.adj = []
        self.w = len(grid[0])
        self.h = len(grid)
        self.grid = grid
        for r, row in enumerate(grid):
            for c, col in enumerate(row):
                adjacent = []
                self.check_add_adj(r, c-1, adjacent)
                self.check_add_adj(r, c+1, adjacent)
                self.check_add_adj(r-1, c, adjacent)
                self.check_add_adj(r+1, c, adjacent)
                self.adj.append(adjacent)

    def check_add_adj(self, r, c, adj):
        if 0 <= r < self.h and 0 <= c < self.w and self.grid[r][c] == 0:
            adj.append(self.to_seq(r, c))

    def to_seq(self, r, c):
        return c + self.h*r

    def get(self, r, c=None):
        n = r
        if c is not None:
            n = self.to_seq(r, c)
        return self.adj[n]

