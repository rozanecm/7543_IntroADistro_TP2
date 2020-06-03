import socket

def start_server(server_address, storage_dir):
  print('TCP: start_server({}, {})'.format(server_address, storage_dir))
  
  port = server_address[1]                              # Puerto
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 + TCP
  host = server_address[0]                              # IP
  s.bind((host, port))
  s.listen(5)

  print ('Server listening....')

  while True:
      conn, addr = s.accept()
      print ('Client connected: ', addr)
      data = conn.recv(1024)
      command = data.decode("utf-8").split(':')
      print('Command received: ', command)

      filename = storage_dir + "\\" + command[1]
      print('Path: ', filename)
      if command[0] == "D":
          file = open(filename,'rb')
          print ('File opened')
          line = file.read(1024)
          while (line):
             conn.send(line)
             #print('Sent ',repr(line))
             line = file.read(1024)

          print('Done sending')
      if command[0] == "U":
          with open(filename, 'wb') as file:
              print ('File opened')
              while True:
                  #print('Receiving data...')
                  data = conn.recv(1024)
                  #print('data=%s', (data))
                  if not data:
                      break
                  # Escribe los datos al archivo
                  file.write(data)

          print('Done receiving')
      file.close()
      print ('File closed')
      conn.close()
      print ('Connection closed')
      pass
#pass
