import settings
import sys
import signal
from grid import Grid
import numpy as np
import socket
import threading
import time
import traceback

PORT = 31337
MSGLEN = len(np.zeros((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, 3), dtype=np.uint8).tobytes())

class Player:

    def __init__(self, color=[255, 0, 0]):
        self.pixels = np.zeros((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, 3))
        self.pixels[0, 0] = color


class Server:

    def __init__(self, *, address):
        self.address = address
        self.grid = Grid(w=settings.SCREEN_WIDTH, h=settings.SCREEN_HEIGHT)
        self.players = {}
        self.acceptor_thread = threading.Thread(target=self._start_listening, name='acceptor-thread')
        self.acceptor_thread.start()
        def shutdown(signum, stack):
            if self.socket is not None:
                print('Server shutdown')
                self.socket.shutdown(socket.SHUT_RDWR)
                self.socket.close()
                sys.exit(0)
        signal.signal(signal.SIGINT, shutdown)
        signal.signal(signal.SIGTERM, shutdown)

    def _start_listening(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.socket = s
            s.bind((self.address, PORT))
            s.listen()
            print('Started listening on %s:%s' % (self.address, PORT))
            while True:
                conn, addr = s.accept()
                self._on_player_connect(client_socket=conn, client_address=addr)

    def get_players(self):
        return self.players

    def get_level(self):
        return self.grid.grid

    def _on_player_connect(self, *, client_socket, client_address):
        print('Player connected from %s [%s]' % (client_address, client_socket))
        self.players[client_address] = (client_socket, Player())

    def send_screen(self, *, screen, client_socket):
        print('Sending screen to %s' % client_socket)
        totalsent = 0
        msg = screen.tobytes()
        while totalsent < MSGLEN:
            sent = client_socket.send(msg[totalsent:])
            if sent == 0:
                print('failed to send a chunk, retrying..')
                continue
            totalsent = totalsent + sent
            print('%s%% sent' % (int((totalsent/MSGLEN))*100))


if __name__ == '__main__':
    s = Server(address='localhost')
    t = 0
    screen = s.get_level()
    while True:
        try:
            if time.time() - t >= 1:
                for client_address, (client_sock, player) in s.players.items():
                    s.send_screen(screen=screen, client_socket=client_sock)
                t = time.time()
        except Exception as e:
            print('Main loop failed')
            traceback.print_exc()
            raise e
