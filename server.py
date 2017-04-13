"""
server
~~~~~~


"""
from __future__ import print_function
import sys
import threading
import socket

from fatalerror import FatalError


class FatalErrorServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        try:
            self.sock.listen(10)
            while True:
                client, addr = self.sock.accept()
                client.settimeout(600)
                threading.Thread(target=self.client_game_instance,
                                 args=(client, addr)).start()
        except (KeyboardInterrupt, socket.error) as e:
            print(e)

    def client_game_instance(self, client, addr):
        new_conn = "[+] New game client connection from {}:{}".format(addr[0],
                                                                      addr[1])
        print(new_conn, end='')

        try:
            s_out = client.makefile('w', 0)
            s_in = client.makefile('r', 0)
            FatalError(s_out, s_in).play()
        except (socket.error, Exception) as e:
            print(e)

        lost_conn = "[-] Lose connection from {}:{}".format(addr[0], addr[1])
        print(lost_conn)

        client.close()

    def __del__(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()


if __name__ == '__main__':
    try:
        FatalErrorServer('127.0.0.1', 9000).listen()
    except socket.error:
        sys.exit(1)
