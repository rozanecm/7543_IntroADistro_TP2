import socket
import hashlib

class Receiver:
    def __init__(self, server_address, chunk_size):
        self.server_address = server_address
        self.chunk_size = chunk_size

    def receive_message(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.server_address)
        self.receive_message(socket)

    # PRE: binded socket
    def receive_message(self, socket):
        self.sock = socket
        
        chunks = {}     # K: seq_num; V: chunk data

        end_of_transmission = False
        while(not end_of_transmission):
            data, address = self.sock.recvfrom(4+self.chunk_size+32)  # 4: seq num; 5: msg size; 32: checksum
            #data = data.decode()
            #print("received", data)
            seq_number = int(data[:4].decode())
            print("read seq num:", seq_number)
            checksum = data[4:4+32].decode()
            msg = data[4+32:]
            print("seq_number", seq_number, "msg", msg, "checksum", checksum)
            if(seq_number == 0):
                end_of_transmission = True
                break
            chunks[seq_number] = msg
            # TODO check integrity
            if(self.checksum_ok(msg, checksum)):
                self.sock.sendto(("ACK" + self.num_to_fix_len_string(seq_number)).encode(), address)
                print("ACK sent")
            print("so far:",chunks)

        print(chunks)
        return self.get_chunks_together(chunks)

    def num_to_fix_len_string(self, num):
        return str(num).zfill(4)

    def get_chunks_together(self, chunks):
        chunk_ids = list(chunks.keys())
        with open("./aux/newtest.txt", 'wb') as file:
            for id in chunk_ids:
                file.write(chunks.pop(id))
                # msg += chunks.pop(id)
        file.close()
        #return msg

    def checksum_ok(self, msg, checksum):
        print("comparing", hashlib.md5(msg).hexdigest(), checksum)
        return hashlib.md5(msg).hexdigest() == checksum


