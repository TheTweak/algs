import settings
from grid import Grid
import numpy as np

class Player:

    def __init__(self, color=[255, 0, 0]):
        self.pixels = np.zeros((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, 3))
        self.pixels[0, 0] = color


class Server:

    def __init__(self, *, address):
        self.address = address
        self.grid = Grid(w=settings.SCREEN_WIDTH, h=settings.SCREEN_HEIGHT)

    def get_players(self):
        return [Player()]

    def get_level(self):
        return self.grid.grid
