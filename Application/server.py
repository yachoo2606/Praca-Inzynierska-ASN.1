import platform
import socket
from _thread import *
import asn1tools

hostname = socket.gethostname()
server = socket.gethostbyname(hostname)

# server = "0.0.0.0"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

asn = asn1tools.compile_files("asn1/modules.asn")

port = 5555

connections = []

try:
    s.bind((server, port))
    print(f"Server Lan IP: {server}")
except socket.error as e:
    print(str(e))

s.listen(2)
print("Waiting for connection, Server Started")


def threaded_game(conn1, conn2):
    print(f"Sent welcome data to {conn1.getpeername()}")
    conn1.send(asn.encode('Connected', {'message': "Connected", 'number': connections.index(conn1), 'connected': True}))
    print(f"Sent welcome data to {conn2.getpeername()}")
    conn2.send(asn.encode('Connected', {'message': "Connected", 'number': connections.index(conn2), 'connected': True}))

    playerTurn = 0
    player1Ready = False
    player2Ready = False

    while not player1Ready and not player2Ready:
        if not player1Ready:
            readyPlayer1Data = conn1.recv(2048)
            if dict(asn.decode('Ready', readyPlayer1Data))['ready']:
                player1Ready = True

        if not player2Ready:
            readyPlayer2Data = conn2.recv(2048)
            if dict(asn.decode('Ready', readyPlayer2Data))['ready']:
                player2Ready = True
        print(f"player1 = {bool(player1Ready)} player2 = {bool(player2Ready)}")

    conn1.send(asn.encode('Ready', {'ready': True}))
    conn2.send(asn.encode('Ready', {'ready': True}))

    while True:
        try:
            data = connections[playerTurn].recv(2048)

            print(f"Receive from Turn Player\n\n")
            print(data)
            print(asn.decode('Request', data))

            connections[not playerTurn].sendall(data)

            print(f"Receive from Second Player\n\n")
            data = connections[not playerTurn].recv(2048)
            print(data)
            print(asn.decode('Response', data))
            # print(asn.decode('Request', data))
            asn1Received = dict(asn.decode('Request', data))
            print(asn1Received)
            connections[playerTurn].sendall(data)

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


def main():
    while True:
        conn1, addr1 = s.accept()
        connections.append(conn1)
        print(connections)
        conn2, addr2 = s.accept()
        connections.append(conn2)
        print(connections)
        print("Connected to:", addr1, addr2)

        start_new_thread(threaded_game, (conn1, conn2))


if __name__ == '__main__':
    main()
