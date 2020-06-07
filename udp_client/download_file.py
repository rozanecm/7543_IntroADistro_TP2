import os

def download_file(server_address, name, dst):
  print('UDP: download_file({}, {}, {})'.format(server_address, name, dst))

  make_storage_dir(dst)

  # TODO make storage dir

  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.bind(server_address)


def make_storage_dir(dst):
    if(not os.path.exists(os.path.dirname(dst))):
        os.mkdir(os.path.dirname(dst))
