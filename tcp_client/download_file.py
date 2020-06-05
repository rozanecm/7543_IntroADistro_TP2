import socket                   # Import socket module
import os

def download_file(server_address, name, dst):
  print('TCP: download_file({}, {}, {})'.format(server_address, name, dst))
  
  make_storage_dir(dst)

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 + TCP
  host = server_address[0]                              # IP
  port = server_address[1]                              # Puerto

  try:
      s.connect((host, port))
  except ConnectionRefusedError:
      print("apparently, server has not been started yet.")
      return 0

  print ('Connected to server')
  print ('Path: ', dst)
  phrase = "D:" + name
  s.send(bytes(phrase, "utf-8"))
  with open(dst, 'wb') as file:
      print ('File opened')
      while True:
          #print('Receiving data...')
          data = s.recv(1024)
          #print('data=%s', (data))
          if not data:
              break
          # write data to a file
          file.write(data)

  print('Done receiving')
  file.close()
  print ('File closed')
  s.close()
  print ('Connection closed')
  #pass

def make_storage_dir(dst):
    if(not os.path.exists(os.path.dirname(dst))):
        os.mkdir(os.path.dirname(dst))
