import socket
import pickle


class LidarDataClient(socket.socket):
    def __init__(self, h, p):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((h, p))

    def get_data(self, dn):
        self.sendall(dn)
        return pickle.loads(self.recv(8192))

    def get_wnt_data(self):
        return self.get_data(b'wnt_data_rq')

    def get_otr_data(self):
        return self.get_data(b'otr_data_rq')
