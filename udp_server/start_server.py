
import argparse
import socket
import time
import os

from utils.md5_hash import md5 as checksum_func
from utils.constants import CHUNK_SIZE
from utils.constants import END_CONNECTION
from utils.constants import START
from utils.constants import NACK
from utils.constants import UPLOAD_COMMAND
from utils.constants import DOWNLOAD_COMMAND

from utils.receiver_udp import Receiver

MAX_RETX = 3
SOCKET_TIMEOUT = 10

def get_timestamp():
  return int(round(time.time()*1000))

def start_server(server_address, storage_dir):
  print('UDP: start_server({}, {})'.format(server_address, storage_dir))

  # si no existe dir, lo crea
  make_storage_dir(storage_dir)

  # Creación del socket UDP.
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.bind(server_address)

  while True:

    # Saco cualquier timeout que pueda tener.
    sock.settimeout(None)

    # Recibo un comando de un cliente, puede ser upload o decode.
    command, addr = sock.recvfrom(CHUNK_SIZE)

    if command.decode() == UPLOAD_COMMAND: 
      upload_file(sock, storage_dir, server_address)

    if command.decode() == DOWNLOAD_COMMAND: 
      download_file(sock)

  sock.close()

def upload_file(sock, storage_dir, server_address):
  my_rec = Receiver(server_address, 1024)
  my_rec.receive_message(sock)
  pass

def download_file():
  pass

def make_storage_dir(storage_dir):
    if(not os.path.isdir(storage_dir)):
        os.mkdir(storage_dir)

