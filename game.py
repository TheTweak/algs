import numpy as np
from matplotlib import pyplot as plt
from grid import Grid

SCREEN_WIDTH = 64
SCREEN_HEIGHT = 64

grid = Grid(w=SCREEN_WIDTH, h=SCREEN_HEIGHT)
def get_level():
    return grid.grid

def get_players():
    return np.zeros((SCREEN_WIDTH, SCREEN_HEIGHT, 3))

def get_screen(server=False):
    screen = np.zeros((SCREEN_WIDTH, SCREEN_HEIGHT, 3))
    level = get_level()
    players = get_players()
    return screen + level + players

if __name__ == '__main__':
    plt.ion()
    plt.gcf().set_size_inches(15, 15)
    while True:
        plt.axis('off')
        plt.imshow(get_screen())
        plt.pause(1e-6)
        plt.clf()
