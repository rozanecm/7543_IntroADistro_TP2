def download_file(server_address, name, dst):
  print('UDP: download_file({}, {}, {})'.format(server_address, name, dst))

  # TODO make storage dir

  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.bind(server_address)
