import socket
import threading
import math
import hashlib

class Sender:
    def __init__(self, server_address, chunk_size):
        self.server_address = server_address
        self.chunk_size = chunk_size
        self.receiver_confirmed_end_of_transmission = False #cuando se manda msj de fin de transmision, el receiver debe confirmar que lo recibio

    def send_message(self, msg):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.send_message(msg, sock)

    def send_message(self, msg, sock, msg_type):
        """
        msg_type: specify if you're sending a command or the body of a msg.
        msg_type can be either "CMD" or "BDY"
        """
        print("working with msg:", msg)
        self.sock = sock
        num_of_chunks = self.get_num_of_chunks_for_msg(msg, self.chunk_size)
        chunks = self.msg_to_chunks(msg, self.chunk_size, num_of_chunks)
        self.acks = list(range(1,num_of_chunks+1))

        send_thread = threading.Thread(target=self.send_file, args=(self.sock,chunks,self.acks,self.server_address,msg_type))
        send_thread.start()
        recv_thread = threading.Thread(target=self.receive_acks, args=(self.sock,self.acks,))
        recv_thread.start()

        send_thread.join()
        recv_thread.join()

    def num_to_fix_len_string(self, num):
        return str(num).zfill(4)

    def send_file(self, sock, chunks, acks, server_address, msg_type):
        while acks:
            print(acks)
            for i in acks:
                print("sending", chunks[i])
                sock.sendto(self.assemble_msg(chunks[i],i), server_address)
        # when finished sending file, send eof msg
        while(not self.receiver_confirmed_end_of_transmission):
            print('sending ack eof')
            sock.sendto(self.assemble_msg(msg_type,0), server_address)
            #sock.sendto(("0000"+msg_type).encode(), server_address)

    def assemble_msg(self, chunk, seq_number):
        seq = self.num_to_fix_len_string(seq_number) 
        ha = hashlib.md5(chunk).hexdigest()
        #ha = hashlib.md5(str(chunk).encode()).hexdigest()
        result = seq.encode() + ha.encode() + chunk
        #result = seq + ha + chunk.decode()
        return result
        #return result.encode()

    def receive_acks(self, sock, acks):
        while acks:
            print("in receiv acks")
            data, addres = sock.recvfrom(3+4)  #3:"ACK"; 4: fixed size seq. num
            data = data.decode()
            try:
                acks.remove(int(data[3:]))
            except ValueError:
                print("try to remove", data[3:], "resulted in error")
        #    print("removed", data[3:], "from acks")

        data, addres = sock.recvfrom(3+4)  #3:"ACK"; 4: fixed size seq. num
        print(data.decode())
        self.receiver_confirmed_end_of_transmission = True

    def get_num_of_chunks_for_msg(self, msg, chunk_size):
        return math.ceil(len(msg) / chunk_size)

    def msg_to_chunks(self, msg, chunk_size, num_of_chunks):
        d = {}
        for i in range(1, num_of_chunks + 1):
            d[i] = msg[:chunk_size]
            msg = msg[chunk_size:]
        return d

