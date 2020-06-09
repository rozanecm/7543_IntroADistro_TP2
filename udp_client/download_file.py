import os
import socket

from utils.constants import CLIENT_ADDRESS
from utils.receiver_udp import Receiver
from utils.sender_udp import Sender


def download_file(server_address, name, dst):
    print('UDP: download_file({}, {}, {})'.format(server_address, name, dst))

    make_storage_dir(dst)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # IPv4 + TCP
    s.bind(CLIENT_ADDRESS)

    print('Path: ', dst)
    phrase = "D:" + name
    sender = Sender(server_address, s)
    sender.send_message(bytes(phrase, "utf-8"))
    with open(dst, 'wb') as file:
        receiver = Receiver(s)
        print('File opened')
        data = receiver.receive_message()
        file.write(data)

    print('Done receiving')
    file.close()
    print('File closed')
    s.close()
    print('Connection closed')
    # pass


def make_storage_dir(dst):
    if (not os.path.exists(os.path.dirname(dst))):
        os.mkdir(os.path.dirname(dst))
