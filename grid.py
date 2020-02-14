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
        for x in range(w):
            row = [0 if random.random() > 0.2 else 1 for _ in range(h)]
            rows.append(row)            
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

