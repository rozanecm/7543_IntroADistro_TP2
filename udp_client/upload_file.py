import os
import argparse
import socket

CHUNK_SIZE=200

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

  sock.sendto(str("upload_file").encode(), server_address)

  signal, addr = sock.recvfrom(CHUNK_SIZE)
  if signal.decode() != "start":
    print("There was an error on the server")
    return exit(1)
  
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

  f.close()
  sock.close()



  pass
