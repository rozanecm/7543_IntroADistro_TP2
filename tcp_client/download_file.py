import socket                   # Import socket module

def download_file(server_address, name, dst):
  print('TCP: download_file({}, {}, {})'.format(server_address, name, dst))
  
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 + TCP
  host = server_address[0]                              # IP
  port = server_address[1]                              # Puerto

  s.connect((host, port))
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
