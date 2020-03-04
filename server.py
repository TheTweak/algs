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
EMPTY_SCREEN = np.zeros((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, 3), dtype=np.uint8)
MSGLEN = len(EMPTY_SCREEN.tobytes())
BUFFER_SIZE = 1024
PLAYER_MOVES = [
        [-1, 0], # 0 - up
        [0, 1],  # 1 - right
        [1, 0],  # 2 - down
        [0, -1], # 3 - left
]

class Player:

    def __init__(self, color=[255, 0, 0]):
        self.pixels = np.copy(EMPTY_SCREEN)
        self.pixels[0, 0] = color
        self.color = color
        self.name = 'playerOne'


class Server:

    def __init__(self, *, address):
        self.address = address
        self.grid = Grid(w=settings.SCREEN_WIDTH, h=settings.SCREEN_HEIGHT)
        # mark bottom right
        self.grid.grid[settings.SCREEN_HEIGHT-1][settings.SCREEN_WIDTH-1] = [0, 255, 0]
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
                self._on_player_connect(player_socket=conn, player_address=addr)

    def get_players(self):
        return self.players

    def get_level(self):
        return self.grid.grid

    def get_screen(self):
        return self.get_all_players_pixels() + self.get_level()

    def get_all_players_pixels(self):
        players_pixels = np.copy(EMPTY_SCREEN)
        for _, p in self.get_players().values():
            players_pixels += p.pixels
        return players_pixels

    def _on_player_connect(self, *, player_socket, player_address):
        print('Player connected from %s [%s]' % (player_address, player_socket))
        color = np.random.randint(255, size=3)
        color[0] = 255
        self.players[player_address] = (player_socket, Player(color=color))

    def send_screen(self, *, screen, player_socket):
        #print('Sending screen to %s' % player_socket)
        totalsent = 0
        msg = screen.tobytes()
        while totalsent < MSGLEN:
            sent = player_socket.send(msg[totalsent:])
            if sent == 0:
                print('failed to send a chunk, retrying..')
                continue
            totalsent = totalsent + sent
            #print('%s%% sent' % (int((totalsent/MSGLEN))*100))

    def recv_player_move(self, *, player_addr, player, player_socket):
        #print('Receiving player move from: %s:%s' % (player_addr[0], player_addr[1]))
        chunks = []
        received = 0
        while received < 1:
            move_bytes = player_socket.recv(BUFFER_SIZE)
            if move_bytes == b'':
                raise RuntimeError('socket connection broken')
            received += len(move_bytes)
        return int.from_bytes(move_bytes, byteorder='big')

    def update_player_coords(self, *, player, move):
        player_coords = np.nonzero(player.pixels)
        move_coords = PLAYER_MOVES[move]
        new_coords = (min(settings.SCREEN_HEIGHT - 1, max(0, player_coords[0][0] + move_coords[0])),
                      min(settings.SCREEN_WIDTH - 1, max(0, player_coords[1][0] + move_coords[1])))
        new_pixels = np.copy(EMPTY_SCREEN)
        new_pixels[new_coords[0], new_coords[1]] = player.color
        collides_with_wall = self.get_level()[new_coords[0], new_coords[1]] == [255, 255, 255]
        if not collides_with_wall.all():
            player.pixels = new_pixels

    def check_connected_shape(self, *, r0=0, r1=settings.SCREEN_WIDTH-1, c0=0, c1=settings.SCREEN_HEIGHT-1,
                              players_pixels):
        for r in range(r0, r1):
            for c in range(c0, c1):
                for p, name in players_pixels:
                    shape = p[r:r+2, c:c+2] 
                    # [255, 255, 255] is a wall color
                    if (shape > 0).all() and (shape != sum([255, 255, 255])).any():
                        print('found connected shape: %s %s [%s]' % (r, c, name))
                        self.grid.grid[r:r+2, c:c+2] = [0, 0, 0]


if __name__ == '__main__':
    s = Server(address='localhost')
    t = 0
    w_chunk = int(settings.SCREEN_WIDTH/1)
    h_chunk = int(settings.SCREEN_HEIGHT/1)
    print('w_chunk=%s, h_chunk=%s' % (w_chunk, h_chunk))
    w_max = settings.SCREEN_WIDTH-1
    h_max = settings.SCREEN_HEIGHT-1
    while True:
        try:
            if time.time() - t >= 1/20:
                frame_time = time.time()
                threads = []
                level_reduced = s.get_level().sum(axis=2)
                players_pixels = []
                for _, p in s.get_players().values():
                    l = level_reduced + p.pixels.sum(axis=2)
                    players_pixels.append((l, p.name))
                for wc in range(0, w_max, w_chunk):
                    for hc in range(0, h_max, h_chunk):
                        args = {'r0': wc,
                                'r1': min(wc+w_chunk, w_max),
                                'c0': hc,
                                'c1': min(hc+h_chunk, h_max),
                                'players_pixels': players_pixels}
                        threads.append(threading.Thread(target=s.check_connected_shape, kwargs=args))
                for t in threads:
                    t.start()
                for t in threads:
                    t.join()
                screen = s.get_screen()
                for player_address, (player_sock, player) in s.players.items():
                    s.send_screen(screen=screen, player_socket=player_sock)
                for player_address, (player_sock, player) in s.players.items():
                    p_move = s.recv_player_move(player_addr=player_address, player=player, player_socket=player_sock)
                    if p_move >= len(PLAYER_MOVES):
                        continue
                    print('player (%s) move is %s' % (player_address, p_move))
                    s.update_player_coords(player=player, move=p_move)
                t = time.time()
                print('frame duration: %s, threads: %s' % (time.time() - frame_time, len(threads)))
        except Exception as e:
            print('Main loop failed')
            traceback.print_exc()
            raise e
