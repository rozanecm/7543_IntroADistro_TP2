
import argparse
import socket
import time

from utils.md5_hash import md5 as checksum_func
from utils.constants import CHUNK_SIZE
from utils.constants import END_CONNECTION
from utils.constants import START
from utils.constants import NACK
from utils.constants import UPLOAD_COMMAND
from utils.constants import DOWNLOAD_COMMAND

MAX_RETX = 3
SOCKET_TIMEOUT = 10

def get_timestamp():
  return int(round(time.time()*1000))

def start_server(server_address, storage_dir):
  print('UDP: start_server({}, {})'.format(server_address, storage_dir))

  # Creación del socket UDP.
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.bind(server_address)

  while True:

    # Saco cualquier timeout que pueda tener.
    sock.settimeout(None)

    # Recibo un comando de un cliente, puede ser upload o decode.
    command, addr = sock.recvfrom(CHUNK_SIZE)

    if command.decode() == UPLOAD_COMMAND: 
      upload_file(sock, storage_dir, addr)

    if command.decode() == DOWNLOAD_COMMAND: 
      download_file(sock)

  sock.close()

def upload_file(sock, storage_dir, client_addr):

  attempts = 0

  # Mando un mensaje al cliente para que empiece con el envío.
  # TODO Acá debería poner un timeout o algún mecanismo para que no se trabe si el mensaje no viene.
  sock.sendto(str(START).encode(), client_addr)

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

  file.truncate()
  # Recibo el tamaño del archivo.
  data, addr = sock.recvfrom(CHUNK_SIZE)
  
  size = try_recieve_size(sock, client_addr, file)

  print("Incoming file with size {} from {}".format(size, addr))
  bytes_received = 0
  # Empieza la transmisión de los datos del archivo.
  while bytes_received < size:

      data, addr = sock.recvfrom(CHUNK_SIZE)

      bytes_received += len(data)
      file.write(data)
  print("File downloaded.")
  file.flush()

  # Mando la cantidad de datos que recibí al cliente.
  sock.sendto(str(bytes_received).encode(),addr)

  # Obtengo el checksum que me calcula el cliente para chequear la integridad.
  src_checksum, addr = sock.recvfrom(CHUNK_SIZE)

  my_checksum = checksum_func(file.name)
  return (my_checksum == src_checksum.decode())


def try_recieve_size(sock, client_addr, file):
  attempt = 0
  recieved = False
  size = 0
  while(attempt < MAX_RETX and not recieved):
    try:
      size = recieve_size(sock, client_addr, file, attempt)
      recieved = True
    except (socket.timeout, ValueError) as e:
      print("Timeout trying to recieve size of message.")
      if(attempt < MAX_RETX):
        print("Reattempting. Attempt {} of {}".format(attempt, MAX_RETX))
        attempt = attempt + 1
        continue
      else:
        raise e
  sock.settimeout(None)
  return size

def recieve_size(sock, client_addr, file, attempt):

  sock.settimeout(SOCKET_TIMEOUT)

  # Recibo el tamaño del archivo.
  data, addr = sock.recvfrom(CHUNK_SIZE)

  size_flag = data.decode()[0:4]

  # Si no recibo el flag "size", es porque no es el mensaje que busco.
  if(size_flag == "SIZE"):
    # Mando la cantidad de datos que recibí al cliente.
    sock.sendto(str("SIZEACK").encode(),addr)
    return int(data.decode()[4:])
  else:
      raise ValueError("Expecting size but get something else: {}".format(data.decode()))


def download_file():
  pass
