
import argparse
import socket
import time
import os
import signal, sys

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
  make_storage_dir(storage_dir)

  # Sin esto no tenemos como salir del loop de forma linda
  signal.signal(signal.SIGINT, sigint_handler)

  # si no existe dir, lo crea
  make_storage_dir(storage_dir)

  # Creación del socket UDP.
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.bind(server_address)

  while True:

    # Saco cualquier timeout que pueda tener.
    sock.settimeout(None)

    print("\nWaiting for next instruction...")
   
    my_rec = Receiver(server_address, 1024)
    data = my_rec.recieve_string(sock, "CMD")

    try:
      if not (data.decode().startswith(UPLOAD_COMMAND) or data.decode().startswith(DOWNLOAD_COMMAND)):
        continue
    except:
      # puse este try por si le llega a llegar un mensaje binario que quedó colgado y falla al hacer el decode
      # simplemente descarta el mensaje y espera al siguiente.
      continue
    
    print("Recieved {}".format(data))
    
    command = data.decode("utf-8").split(':')

    filename = os.path.join(storage_dir, command[1])

    if command[0] == UPLOAD_COMMAND: 
      upload_file(sock, storage_dir, server_address, filename)

    if command[0] == DOWNLOAD_COMMAND: 
      download_file(sock)

  sock.close()

def upload_file(sock, storage_dir, server_address, filename, reciever):
  reciever.receive_message(sock, filename)

def download_file():
  pass

def make_storage_dir(storage_dir):
    if(not os.path.isdir(storage_dir)):
        os.mkdir(storage_dir)

def make_storage_dir(storage_dir):
    if(not os.path.isdir(storage_dir)):
        os.mkdir(storage_dir)

def sigint_handler(sig, frame):
    sys.exit(0)

