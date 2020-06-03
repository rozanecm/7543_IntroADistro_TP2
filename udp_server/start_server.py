
import argparse
import socket
import time

CHUNK_SIZE = 200

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

  # Mando un mensaje al cliente para que empiece con el envío.
  # TODO Acá debería poner un timeout o algún mecanismo para que no se trabe si el mensaje no viene.
  sock.sendto(str("start").encode(), client_addr)

  # Recibo el tamaño del archivo.
  data, addr = sock.recvfrom(CHUNK_SIZE)
  size = int(data.decode())
  print("Incoming file with size {} from {}".format(size, addr))

  # Creo un archivo en el "servidor"
  filename = "{}/file-{}.bin".format(storage_dir, get_timestamp())
  f = open(filename, "wb")
  bytes_received = 0

  # empieza la transmisión de los datos del archivo.
  while bytes_received < size:
      data, addr = sock.recvfrom(CHUNK_SIZE)
      bytes_received += len(data)
      f.write(data)
  f.close()

  print("Received file {}".format(filename))

  # Para finalizar mando la cantidad de datos que recibí al cliente
  sock.sendto(str(bytes_received).encode(),addr)


def download_file():
  pass
