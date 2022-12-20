import socket
from _thread import *
import random
import asn1tools

server = "127.0.0.1"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

asn = asn1tools.compile_files("asn1/modules.asn")

port = 5555

connections = []
oneEndedConnection = False
playerTurn = 0

try:
    s.bind((server, port))
    print(f"Server Lan IP: {socket.gethostbyname(socket.gethostname())}")
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for connection, Server Started")


def threaded_client(conn):
    print(f"sended welcome data to {conn.getpeername()}")
    conn.send(asn.encode('Connected', {'message': "Connected", 'number': connections.index(conn), 'connected': True}))

    while True:
        try:
            data = conn.recv(2048)

            print(f"Receive from Turn Player\n\n")
            print(data)
            print(asn.decode('Request', data))
            # print(asn.decode('Request', data))
            asn1Receivd = dict(asn.decode('Request', data))

            # connections[not playerTurn].sendall(data)
            #
            # print(f"Receive from Second Player\n\n")
            # data = connections[not playerTurn].recv(2048)
            # print(data)
            # print(asn.decode('Response', data))
            # # print(asn.decode('Request', data))
            # asn1Receivd = dict(asn.decode('Request', data))
            # print(asn1Receivd)
            # connections[playerTurn].sendall(data)
            conn.sendall(
                asn.encode('Response', {'hit': True, 'column': asn1Receivd['column'], 'row': asn1Receivd['row']}))

        except Exception as inst:
            print(inst)
            print(inst.args)
            break
    print("Lost connection")
    connections.remove(conn)
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()


while True:
    conn, addr = s.accept()
    connections.append(conn)
    print(connections)
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn,))
