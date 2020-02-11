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

