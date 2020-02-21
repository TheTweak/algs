import settings
from grid import Grid
import numpy as np
import socket

PORT = 31337

class Player:

    def __init__(self, color=[255, 0, 0]):
        self.pixels = np.zeros((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, 3))
        self.pixels[0, 0] = color


class Server:

    def __init__(self, *, address):
        self.address = address
        self.grid = Grid(w=settings.SCREEN_WIDTH, h=settings.SCREEN_HEIGHT)
        self.players = {}
        self._start_listening()

    def _start_listening(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.address, PORT))
            s.listen()
            print('Started listening on %s:%s' % (self.address, PORT))
            conn, addr = s.accept()
            with conn:
                self._on_player_connect(connection=conn, client_address=addr)

    def get_players(self):
        return self.players

    def get_level(self):
        return self.grid.grid

    def _on_player_connect(self, *, connection, client_address):
        print('Player connected from %s [%s]' % (client_address, connection))
        self.players[connection] = Player()


if __name__ == '__main__':
    Server(address='localhost')
