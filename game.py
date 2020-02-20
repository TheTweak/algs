import numpy as np
from matplotlib import pyplot as plt
from grid import Grid
import argparse
from server import Server
import settings

def get_players():
    pixels = np.zeros((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, 3))
    pixels[settings.PLAYER_SPAWN_Y, settings.PLAYER_SPAWN_X] = [255, 0, 0]
    return pixels

def get_screen(server):
    screen = np.zeros((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, 3))
    screen += server.get_level()
    players = server.get_players()
    for p in players:
        screen += p.pixels
    return screen

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-server', help='Server address', default='localhost')
    args = parser.parse_args()
    server = Server(address=args.server)
    plt.ion()
    plt.gcf().set_size_inches(15, 15)
    while True:
        plt.axis('off')
        plt.imshow(get_screen(server))
        plt.pause(1e-6)
        plt.clf()
