import socket
import time
import os
import signal, sys

from utils.constants import CLIENT_ADDRESS
from utils.receiver_udp import Receiver
from utils.sender_udp import Sender

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
        
        try:
            command = data.decode("utf-8").split(':')
            print('Command received: ', command)
        except:
            #not a valid command.
            continue
        
        if(not validate_command(command[0])):
            continue

        filename = os.path.join(storage_dir, command[1])
        print('Path: ', filename)
        if command[0] == "D":
            sender = Sender(CLIENT_ADDRESS, s)
            try:
                file = open(filename, 'rb')
            except:
                print('File request does not exist in the server.')
                sender.send_message("")
                #if file does not exist, do not fail.
                continue

            print('File opened')
            msg = file.read()
            sender.send_message(msg)

            print('Done sending')
        if command[0] == "U":
            with open(filename, 'wb') as file:
                print('File opened')
                msg = conn.receive_message()
                file.write(msg)
                file.close()

            print('Done receiving')

        print('File closed')

def validate_command(command):
    return command.startswith("D") or command.startswith("U")

def make_storage_dir(storage_dir):
    if (not os.path.isdir(storage_dir)):
        os.mkdir(storage_dir)
