from matplotlib import pyplot as plt
import numpy as np
import random
import time

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
        rows = []
        for x in range(h):
            row = [0 for _ in range(w)]
            rows.append(row)            
        block_size = int(w/5)
        block_directions = [0, 1, 2, 3] # do nothing, down, left, right
        for bx in range(0, h, block_size):
            for by in range(0, w, block_size): 
                block_length = random.randint(0, block_size)
                blocks = []
                for _ in range(block_length):
                    blocks.append(random.choice(block_directions))
                for bi, b in enumerate(blocks):
                    if b == 0:
                        pass
                    elif b == 1:
                        rows[min(h-1, bx+bi+1)][by] = 1
                    elif b == 2:
                        rows[bx][min(w-1, max(0, by+bi-1))] = 1
                    elif b == 3:
                        rows[bx][min(by+bi+1, w-1)] = 1
        # top left and bottom right is always 0
        rows[0][0] = 0
        rows[len(rows)-1][len(rows)-1] = 0
        return rows

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

