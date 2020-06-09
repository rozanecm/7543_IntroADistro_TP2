import socket
import time
import os
import signal, sys

from utils.receiver_udp import Receiver

MAX_RETX = 3
SOCKET_TIMEOUT = 10


def get_timestamp():
    return int(round(time.time() * 1000))


def start_server(server_address, storage_dir):
    print('UDP: start_server({}, {})'.format(server_address, storage_dir))
    make_storage_dir(storage_dir)

    # port = server_address[1]  # Puerto
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # IPv4 + TCP
    # host = server_address[0]  # IP
    s.bind(server_address)

    print('Server listening....')


    def sigint_handler(sig, frame):
        print("received signal")
        s.close()
        print('Connection closed')
        sys.exit(0)

    signal.signal(signal.SIGINT, sigint_handler)
    while True:
        conn = Receiver(s)
        data = conn.receive_message()
        print("data:", data)
        command = data.decode("utf-8").split(':')
        print('Command received: ', command)

        filename = os.path.join(storage_dir, command[1])
        print('Path: ', filename)
        if command[0] == "D":
            file = open(filename, 'rb')
            print('File opened')
            line = file.read(1024)
            while (line):
                try:
                    conn.send(line)
                except (ConnectionResetError, BrokenPipeError):
                    line = False
                # print('Sent ',repr(line))
                line = file.read(1024)

            print('Done sending')
        if command[0] == "U":
            with open(filename, 'wb') as file:
                print('File opened')
                msg = conn.receive_message()
                file.write(msg)
                file.close()

            print('Done receiving')

        print('File closed')


def make_storage_dir(storage_dir):
    if (not os.path.isdir(storage_dir)):
        os.mkdir(storage_dir)
