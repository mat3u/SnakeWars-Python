import socket
import json
from pprint import pprint
import time

HOST = "127.0.0.1"
PORT = 9977
PLAYER = "PL2"

MOVES = ["LEFT", "RIGHT", "STRAIGHT"]

def play(id, state):
    # --- YOUR CODE GOES HERE ---
    pprint(state)
    return "STRAIGHT"

    # --- YOUR CODE ENDS HERE ---


# --- SAD TCP CLIENT ---
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    s.connect((HOST, PORT))

    def send(msg):
        s.sendall((msg + "\n").encode('ascii'))

    def recv(buffer=4096):
        return s.recv(buffer, ).decode("ascii").strip()

    def recvline():
        resp = bytearray()
        while True:
            chunk = s.recv(128)
            resp.extend(chunk)
            if b'\n' in chunk or not chunk:
                break

        return resp[:resp.find(b'\n')].decode('ascii').strip()

    hello = recv(128)

    if hello != "ID":
        print(
            "ERROR: Server responded with incorrect handshake: [{}]".format(hello))
        exit(1)

    send(PLAYER)

    ID = recv(128)

    print("Your player is {}".format(ID))

    while True:
        try:
            start_t = time.time()
            raw = recvline()
            state = json.loads(raw)

            move_t = time.time()
            move = play(ID, state)

            send(move)

            end_t = time.time()

            print(move, "; c: ", end_t-start_t, ", u:", end_t-move_t)
        except Exception as e:
            print("ERROR:", e, e.args)
