
import argparse
import socket
import time

from utils.md5_hash import md5 as checksum_func
from utils.constants import CHUNK_SIZE
from utils.constants import END_CONNECTION
from utils.constants import START
from utils.constants import NACK

MAX_RETX = 3

def get_timestamp():
  return int(round(time.time()*1000))

def start_server(server_address, storage_dir):
  print('UDP: start_server({}, {})'.format(server_address, storage_dir))

  # Creación del socket UDP.
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.bind(server_address)

  while True:

    # Recibo un comando de un cliente, puede ser upload o decode.
    command, addr = sock.recvfrom(CHUNK_SIZE)

    if command.decode() == "upload_file": 
      upload_file(sock, storage_dir, addr)

    if command.decode() == "download_file": 
      download_file(sock)

  sock.close()

def upload_file(sock, storage_dir, client_addr):

  attempts = 0

  # Mando un mensaje al cliente para que empiece con el envío.
  # TODO Acá debería poner un timeout o algún mecanismo para que no se trabe si el mensaje no viene.
  sock.sendto(str("start").encode(), client_addr)

  # Creo un archivo temporal en el "servidor"
  filename = "{}/file-{}.bin".format(storage_dir, get_timestamp())
  f = open(filename, "wb")

  # intenta tres veces de subir el archivo.
  while(attempts < MAX_RETX and not (try_to_recieve(sock, client_addr, f))):
    
    # pido que retransmita
    sock.sendto("nack".encode(),client_addr)
    print("Checksum didn't match, reatempting. Attempt: {} of {}".format(attempts, MAX_RETX))
    attempts = attempts + 1 

  f.close()

  # fin de la conexión.
  sock.sendto("bye".encode(),client_addr)

  print("Received file {}".format(filename))

  
def try_to_recieve(sock, client_addr, file):

  # Recibo el tamaño del archivo.
  data, addr = sock.recvfrom(CHUNK_SIZE)
  size = int(data.decode())
  print("Incoming file with size {} from {}".format(size, addr))
  bytes_received = 0
  # empieza la transmisión de los datos del archivo.
  while bytes_received < size:
      data, addr = sock.recvfrom(CHUNK_SIZE)
      bytes_received += len(data)
      file.write(data)
  print("File downloaded")

  # Mando la cantidad de datos que recibí al cliente.
  sock.sendto(str(bytes_received).encode(),addr)

  # Obtengo el checksum que me calcula el cliente para chequear la integridad.
  src_checksum, addr = sock.recvfrom(CHUNK_SIZE)

  my_checksum = checksum_func(file.name)
  return (my_checksum == src_checksum)


def download_file():
  pass
