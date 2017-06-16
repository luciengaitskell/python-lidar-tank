import socket
import pickle
import threading
import time


class LidarDataClient(socket.socket):
    def __init__(self, h, p):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((h, p))

        self.data = {'sweep_wnt': [], 'sweep_otr': []}

        self.running = False
        self.dt = threading.Thread(target=self.data_helper)

    def __enter__(self):
        super().__enter__()
        self.running = True
        self.dt.start()
        return self

    def __exit__(self, *args, **kwargs):
        super().__exit__(*args, **kwargs)
        self.running = False
        self.dt.join()

    def data_helper(self):
        while self.running:
            self.data = self.get_data(b'all_data')
            time.sleep(0.1)

    def get_data(self, dn):
        self.sendall(dn)
        bs = b''
        while True:
            nd = self.recv(8192)
            bs += nd
            if nd[-1:] == b'\x03':
                return pickle.loads(bs)
