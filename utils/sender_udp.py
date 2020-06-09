import socket
import threading
import math
import hashlib

from utils.constants import CHUNK_SIZE

class Sender:
    def __init__(self, server_address, sock):
        self.server_address = server_address
        self.sock = sock
        # binding is neede to receive data
        # self.sock.bind(("127.0.0.1",2020))

    def send_message(self, msg):
        """
        :param msg: must be bin, not text
        :return: void
        """
        print("working with msg:", msg)
        num_of_chunks = self.get_num_of_chunks_for_msg(msg)
        chunks = self.msg_to_chunks(msg, num_of_chunks)
        acks = list(range(num_of_chunks+1))

        self.sock.settimeout(1)
        # self.sock.setblocking(0)
        while acks:
            aux_acks = acks[:]
            for i in aux_acks:
                self.sock.sendto(self.assemble_msg(chunks[i],i), self.server_address)
                print("just sent:", self.assemble_msg(chunks[i],i))
                try:
                    data, address = self.sock.recvfrom(4 + 3)  # 4: fixed size seq. num; 3:"ACK"
                    # data = data.decode()
                except socket.timeout:
                    break
                try:
                    # if duplicate ack received, it'll try to remove inexisteint
                    # element. Prevent with this catch
                    acks.remove(int(data[:4]))
                except ValueError:
                    continue
        print("just sent msg:", msg)


    @staticmethod
    def num_to_fix_len_string(num):
        return str(num).zfill(4)

    def assemble_msg(self, chunk, seq_number):
        seq = self.num_to_fix_len_string(seq_number) 
        ha = hashlib.md5(chunk).hexdigest()
        # ha = hashlib.md5(str(chunk).encode()).hexdigest()
        result = seq.encode() + ha.encode() + chunk
        # result = seq + ha + chunk.decode()
        return result
        # return result.encode()

    def get_num_of_chunks_for_msg(self, msg):
        return math.ceil(len(msg) / CHUNK_SIZE)

    def msg_to_chunks(self, msg, num_of_chunks):
        """
        :param msg: binary msg
        :param num_of_chunks: num of chunks to be sent
        :return: dict with message split to chunks, where k = seq. number and v = chunk.
        seq n. 0 transmits number of packets needed to transmit the message
        """
        d = {}
        for i in range(1, num_of_chunks + 1):
            d[i] = msg[:CHUNK_SIZE]
            msg = msg[CHUNK_SIZE:]
        d[0] = str(num_of_chunks).encode()
        return d

