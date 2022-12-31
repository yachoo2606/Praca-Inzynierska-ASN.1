import socket

import asn1tools


class Network:
    def __init__(self, ADDRESS="127.0.0.1"):
        self.asn = asn1tools.compile_files('asn1/modules.asn')
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ADDRESS
        self.port = 5555
        self.addr = (self.server, self.port)
        self.pos = self.connect()

    def get_pos(self):
        return self.pos

    def connect(self):
        try:
            self.client.connect(self.addr)
            data = dict(self.asn.decode("Connected", self.client.recv(2048)))
            print(data)
            return data['number']
        except:
            pass

    def send(self, data):
        try:
            # self.client.send(str.encode(data))
            print(data)
            self.client.send(data)
            return self.client.recv(2048)
        except socket.error as e:
            print(e)
