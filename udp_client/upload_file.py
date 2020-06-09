import os
import socket

from utils.sender_udp import Sender
from utils.receiver_udp import Receiver

# timeout grande para testear
SOCKET_TIMEOUT = 10
MAX_RETX = 10


def upload_file(server_address, src, name):
    # TODO: Implementar UDP upload_file client
    print('UDP: upload_file({}, {}, {})'.format(server_address, src, name))

    if (not os.path.exists(src)):
        print("Please enter valid file to upload")
        return 0

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # IPv4 + TCP
    host = server_address[0]  # IP
    port = server_address[1]  # Puerto

    phrase = "U:" + name
    print("phrase:", phrase)
    sender = Sender(server_address, s)
    sender.send_message(bytes(phrase, "utf-8"))

    # wait for "ack" so command doesn't get mixed with sent file
    # sys.sl

    print('Path: ', src)
    file = open(src, 'rb')
    print('File opened')
    sender.send_message(file.read())
    print('Done sending')
    file.close()
    print('File closed')
    s.close()
    print('Connection closed')
