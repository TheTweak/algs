import socket
import numpy as np
from matplotlib import pyplot as plt
import argparse
import settings
import matplotlib as mpl

# remove default keybinding for 's'
mpl.rcParams['keymap.save'].remove('s')

MSGLEN = len(np.zeros((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, 3), dtype=np.uint8).tobytes())
BUFFER_SIZE = 1024
MOVE = 4
KEY_MAP = {
        'w': 0, # up
        'd': 1, # right
        's': 2, # down
        'a': 3  # left
}

class Client:

    def __init__(self, *, server):
        self.server = server
        print('Connecting to %s..' % server)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((server, 31337))

    def get_screen(self):
        chunks = []
        received = 0
        while received < MSGLEN:
            chunk = self.socket.recv(min(BUFFER_SIZE, MSGLEN - received))
            if chunk == b'':
                raise RuntimeError('socket connection broken')
            chunks.append(chunk)
            received += len(chunk)
            #print('Received %s%% of screen..' % (int((received / MSGLEN)*100)))
        msg = b''.join(chunks)
        return np.frombuffer(msg, dtype=np.uint8).reshape((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT, 3))

    def send_move(self, move):
        # 0 - up, 1 - right, 2 - down, 3 - left
        print('Sending move %s' % move)
        totalsent = 0
        msg = move.to_bytes(1, byteorder='big')
        while totalsent < 1:
            sent = self.socket.send(msg)
            if sent == 0:
                print('failed to send a chunk, retrying..')
                continue
            totalsent = totalsent + sent

def key_pressed(event):
    print('key pressed: %s' % event.key)
    global MOVE
    if event.key in KEY_MAP:
        MOVE = KEY_MAP[event.key]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-server', help='Server address', default='localhost')
    args = parser.parse_args()
    try:
        client = Client(server=args.server)
        plt.ion()
        plt.gcf().set_size_inches(30, 30)
        plt.gcf().canvas.mpl_connect('key_press_event', key_pressed)
        while True:
            plt.axis('off')
            plt.imshow(client.get_screen())
            plt.pause(1e-6)
            plt.clf()
            client.send_move(MOVE)
            MOVE = 4
    except Exception as e:
        print('Client failed: %s' % e)
        client.socket.close()
        raise e
