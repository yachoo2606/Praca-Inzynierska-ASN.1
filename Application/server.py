import socket
from _thread import *
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


def threaded_client(conn1,conn2):
    print(f"sended welcome data to {conn1.getpeername()}")
    conn1.send(asn.encode('Connected', {'message': "Connected", 'number': connections.index(conn1), 'connected': True}))
    print(f"sended welcome data to {conn2.getpeername()}")
    conn2.send(asn.encode('Connected', {'message': "Connected", 'number': connections.index(conn2), 'connected': True}))

    global playerTurn

    while True:
        try:
            data = connections[playerTurn].recv(2048)

            print(f"Receive from Turn Player\n\n")
            print(data)
            print(asn.decode('Request', data))
            asn1Receivd = dict(asn.decode('Request', data))

            connections[not playerTurn].sendall(data)

            print(f"Receive from Second Player\n\n")
            data = connections[not playerTurn].recv(2048)
            print(data)
            print(asn.decode('Response', data))
            # print(asn.decode('Request', data))
            asn1Receivd = dict(asn.decode('Request', data))
            print(asn1Receivd)
            connections[playerTurn].sendall(data)
            # connections[playerTurn].sendall(
            #     asn.encode('Response', {'hit': True, 'column': asn1Receivd['column'], 'row': asn1Receivd['row']}))
            playerTurn = not playerTurn


        except Exception as inst:
            print(inst)
            print(inst.args)
            break
    print("Lost connection")
    connections.remove(conn1)
    connections.remove(conn2)
    conn1.shutdown(socket.SHUT_RDWR)
    conn2.shutdown(socket.SHUT_RDWR)
    conn1.close()
    conn2.close()


while True:
    conn1, addr1 = s.accept()
    connections.append(conn1)
    print(connections)
    conn2, addr2 = s.accept()
    connections.append(conn2)
    print(connections)
    print("Connected to:", addr1, addr2)

    start_new_thread(threaded_client, (conn1,conn2))
