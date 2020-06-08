import os
import argparse
import socket

from utils.md5_hash import md5 as checksum_func
from utils.constants import CHUNK_SIZE
from utils.constants import END_CONNECTION
from utils.constants import START
from utils.constants import NACK
from utils.constants import UPLOAD_COMMAND
from utils.constants import DOWNLOAD_COMMAND

from utils.sender_udp import Sender

#timeout grande para testear
SOCKET_TIMEOUT = 10
MAX_RETX = 10

def upload_file(server_address, src, name):
  # TODO: Implementar UDP upload_file client
  print('UDP: upload_file({}, {}, {})'.format(server_address, src, name))

  if(not os.path.exists(src)):
      print("Please enter valid file to upload")
      return 0

  own_address = ("127.0.0.1", 2020)

  f = open(src, "rb")
  #f = open(name, "rb")
  f.seek(0, os.SEEK_END)
  size = f.tell()
  f.seek(0, os.SEEK_SET)

  print("Sending {} bytes from {}".format(size, name))

  # Create socket and connect to server
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.bind(own_address)

  command = "{}:{}".format(UPLOAD_COMMAND, name)
  
  print(command)

  my_sen = Sender(server_address, 1024)
  my_sen.send_message(command.encode(), sock, "CMD")

  f = open(src, "rb")   
  #f = open("./files/cover.jpg", "rb")   
  my_sen.send_message(f.read(), sock, "BDY")

  f.close()
  
  sock.close()
  pass




  
