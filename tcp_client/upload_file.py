import socket
import os

def upload_file(server_address, src, name):
  print('TCP: upload_file({}, {}, {})'.format(server_address, src, name))

  if(not os.path.exists(src)):
      print("Please enter valid file to upload")
      return 0

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # IPv4 + TCP
  host = server_address[0]                              # IP
  port = server_address[1]                              # Puerto

  try:
      s.connect((host, port))
  except ConnectionRefusedError:
      print("apparently, server has not been started yet.")
      return 0

  print ('Connected to server')
  phrase = "U:" + name
  print("phrase:", phrase)
  s.send(bytes(phrase, "utf-8"))

  # wait for "ack" so command doesn't get mixed with sent file
  s.recv(1024)

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
