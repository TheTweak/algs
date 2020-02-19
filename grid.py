from matplotlib import pyplot as plt
import numpy as np
import random
import time
import itertools

class Grid:

    def __init__(self, w=5, h=5):
        self.h = h
        self.w = w
        s = time.time()
        self.data = self.generategrid(w=w, h=h)
        self.grid = np.zeros((h, w, 3), dtype=np.uint8)
        print("Grid data generated in %s" % (time.time() - s))
        for x, r in enumerate(self.data):
            for y, c in enumerate(r):
                if c == 0:
                    self.grid[x, y] = [0, 255, 0]

    def generategrid(self, w=5, h=5):
        rows = [[0]*w for _ in range(h)]
        block_size = int(w/8)
        for x in range(0, w, block_size):
            for y in range(0, h, block_size):
                block = self.generateblock(block_size)
                for bx, brow in enumerate(block):
                    for by, b in enumerate(brow):
                        if x+bx >= w or y+by >= h:
                            continue
                        rows[x+bx][y+by] = b
        # top left and bottom right is always 0
        rows[0][0] = 0
        rows[len(rows)-1][len(rows)-1] = 0
        return rows

    def generateblock(self, size):
        x = random.randint(0, size) # starting point
        y = random.randint(0, size)
        directions = list(itertools.product([0, 1, -1], [0, 1, -1]))
        block = [[0]*size for _ in range(size)]
        for _ in range(size):
            dx, dy = random.choice(directions)
            x += dx
            y += dy
            x = max(0, x)
            x = min(x, size-1)
            y = max(0, y)
            y = min(y, size-1)
            block[x][y] = 1
        return block

    '''
    Change color of cell V (sequential number)
    '''
    def set_cell_color(self, *, v, color):
        x = int(v / self.w)
        y = v - x * self.w
        self.grid[x, y] = color

    def show(self):
        plt.imshow(self.grid)
        plt.show()


if __name__ == "__main__":
    g = Grid(w=32, h=32)
    g.show()
