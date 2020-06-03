import socket

def upload_file(server_address, src, name):
  print('TCP: upload_file({}, {}, {})'.format(server_address, src, name))

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 + TCP
  host = server_address[0]                              # IP
  port = server_address[1]                              # Puerto

  s.connect((host, port))
  print ('Connected to server')
  phrase = "U:" + name
  s.send(bytes(phrase, "utf-8"))

  print('Path: ', src)
  file = open(src,'rb')
  print ('File opened')
  line = file.read(1024)
  while (line):
    s.send(line)
    #print('Sent ',repr(line))
    line = file.read(1024)
  print('Done sending')
  file.close()
  print ('File closed')
  s.close()
  print('Connection closed')
#  pass
