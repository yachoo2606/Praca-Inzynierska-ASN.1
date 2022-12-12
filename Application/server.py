import socket
from _thread import *
import random
import sys

server = "127.0.0.1"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 5555

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for connection, Server Started")


def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


pos = [(0, 0), (0, 0)]


def threaded_client(conn, currentPlayer):
    conn.send(str.encode("Connected"))
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[currentPlayer] = data
            print(data)

            if not data:
                print("Disconnected")
                break
            else:
                reply = (random.randint(0, 9), random.randint(0, 9))
                print(reply)
                # if player == 1:
                #     reply = pos[0]
                # else:
                #     reply = pos[1]
                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(str.encode(make_pos(reply)))
        except:
            break
    print("Lost connection")
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1