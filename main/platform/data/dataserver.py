import asyncore
import socket
import pickle
import threading

sweep_wnt = []
sweep_otr = []


class DataHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        data = self.recv(8192)
        if data == b'wnt_data_rq':
            self.send(pickle.dumps(sweep_wnt))
        elif data == b'otr_data_rq':
            self.send(pickle.dumps(sweep_otr))


class DataServer(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            return
        else:
            sock, addr = pair
            print('Incoming connection from %s' % repr(addr))
            handler = DataHandler(sock)


def start():
    s = DataServer('', 8080)
    t = threading.Thread(target=asyncore.loop, kwargs={'timeout': 1})
    t.start()
    return s, t
