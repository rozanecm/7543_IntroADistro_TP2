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
  
  
  response = try_to_send(sock, size, server_address, f)
  
  print("Response from server {}".format(response))
  
  #try again
  if(response == NACK):
    print("Send again")
    response = try_to_send(sock, size, server_address, f)

  f.close()
  sock.close()
  pass


def try_to_send(sock, size, server_address, f):
  
  # Rebobino el archivo
  f.seek(0, os.SEEK_END)
  size = f.tell()
  f.seek(0, os.SEEK_SET)

  #Envío primero el tamaño del archivo para leerlo del lado del servidor.
  #TODO deberíamos agregar un hash al mensaje de tamaño fijo tipo checksum.
  sock.sendto(str(size).encode(), server_address)

  # Mando todo el archivo.
  while True:
    chunk = f.read(CHUNK_SIZE)
    if not chunk:
      break
    sock.sendto(chunk, server_address)

  # El server me dice cuánta data recibió.
  num_bytes, addr = sock.recvfrom(CHUNK_SIZE)

  print("Server received {} bytes".format(num_bytes.decode()))

  checksum = "12434"
  print("Sending checksum: {}".format(checksum))

  sock.sendto(checksum.encode(), server_address)

  signal, addr = sock.recvfrom(CHUNK_SIZE)

  return signal.decode()
