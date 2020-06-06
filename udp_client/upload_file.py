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

#timeout grande para testear
SOCKET_TIMEOUT = 10
MAX_RETX = 10

def upload_file(server_address, src, name):
  # TODO: Implementar UDP upload_file client
  print('UDP: upload_file({}, {}, {})'.format(server_address, src, name))

  #hago esto medio mock para triggerear acciones y probar mi servidor.

  own_address = ("127.0.0.1", 2020)

  f = open(name, "rb")
  f.seek(0, os.SEEK_END)
  size = f.tell()
  f.seek(0, os.SEEK_SET)

  print("Sending {} bytes from {}".format(size, name))

  # Create socket and connect to server
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.bind(own_address)

  sock.sendto(str(UPLOAD_COMMAND).encode(), server_address)

  signal, addr = sock.recvfrom(CHUNK_SIZE)
  if signal.decode() != START:
    print("There was an error on the server")
    return exit(1)
  
  
  response = try_to_send_file(sock, size, server_address, f)
  
  print("Response from server {}".format(response))
  
  #try again
  if(response == NACK):
    print("Send again")
    response = try_to_send_file(sock, size, server_address, f)

  f.close()
  sock.close()
  pass


def try_to_send_file(sock, size, server_address, f):
  
  # Rebobino el archivo
  f.seek(0, os.SEEK_END)
  size = f.tell()
  f.seek(0, os.SEEK_SET)

  try:
    try_send_size(sock, size, server_address)
  except (socket.timeout, ValueError) as e:
    print("Unfortunately the server is experiencing some problems, try again later.")
    return
  
  sock.settimeout(None)

  print("Ready to send file.")

  # Mando todo el archivo.
  while True:
    chunk = f.read(CHUNK_SIZE)
    if not chunk:
      break
    sock.sendto(chunk, server_address)

  # El server me dice cuánta data recibió.
  num_bytes, addr = sock.recvfrom(CHUNK_SIZE)

  print("Server received {} bytes".format(num_bytes.decode()))

  checksum = checksum_func(f.name)
  print("Sending checksum: {}".format(checksum))

  sock.sendto(checksum.encode(), server_address)

  signal, addr = sock.recvfrom(CHUNK_SIZE)

  return signal.decode()

def try_send_size(sock, size, server_address):
  attempt = 0
  sent = False
  while(attempt < MAX_RETX and not sent):
    try:
      send_size(sock, size, server_address, attempt)
      sent = True
    except (socket.timeout, ValueError) as e:
      print("Timeout trying to recieve size of message.")
      if(attempt < MAX_RETX):
        print("Reattempting. Attempt {} of {}".format(attempt, MAX_RETX))
        attempt = attempt + 1
        continue
      else:
        raise e
  return sent

def send_size(sock, size, server_address, attempt):

  print("Sending size of file to server: {}.".format(size))
  message = "SIZE{}".format(str(size))
  sock.sendto(message.encode(), server_address)
  
  sock.settimeout(SOCKET_TIMEOUT)

  # Recibo la confirmación del servidor, puede dar timeout pero lo manejo afuera de esta función
  # junto con el manejo de retries.
  data, addr = sock.recvfrom(CHUNK_SIZE)
  ack = data.decode()
  
  if(ack == "SIZEACK"):
    print("Size message sent correctly.")
    return True
  else:
    print("Wrong ack recieved: {}".format(ack))
    raise ValueError("Wrong ack recieved: {}".format(ack))

  