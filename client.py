import socket
import numpy as np
from matplotlib import pyplot as plt
import argparse
import settings

def get_screen(client):
    screen = np.zeros((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, 3))
    '''screen += client.get_level()
    players = client.get_players()
    for p in players:
        screen += p.pixels'''
    return screen

class Client:

    def __init__(self, *, server):
        self.server = server
        print('Connecting to %s..' % server)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server, 31337))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-server', help='Server address', default='localhost')
    args = parser.parse_args()
    try:
        client = Client(server=args.server)
        plt.ion()
        plt.gcf().set_size_inches(15, 15)
        while True:
            plt.axis('off')
            plt.imshow(get_screen(client))
            plt.pause(1e-6)
            plt.clf()
    except Exception as e:
        print('Client failed: %s' % e)
        client.sock.close()
        raise e
