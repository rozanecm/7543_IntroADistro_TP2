import hashlib
from utils.constants import CHUNK_SIZE

class Receiver:
    def __init__(self, sock):
        self.sock = sock

    # PRE: binded socket
    def receive_message(self):
        chunks = self.receive()
        return self.get_chunks_together(chunks)

    def num_to_fix_len_string(self, num):
        return str(num).zfill(4)

    def get_chunks_together(self, chunks):
        chunk_ids = list(chunks.keys())
        msg = b""
        for id in chunk_ids:
            msg += chunks.pop(id)
        return msg

    def checksum_ok(self, msg, checksum):
        return hashlib.md5(msg).hexdigest() == checksum

    def recieve_string(self, sock, msg_type):
        """
        msg_type: specify whether you're receiving a command ("CMD") or the
        body of a msg ("BDY"). This serves the purpose to detect the correct
        end of transmission.
        """
        return self.get_chunks_together_in_string(self.receive())

    # PRE: binded socket
    def receive(self):
        chunks = {}     # K: seq_num; V: chunk data

        num_of_pkts_received = 0
        end_of_transmission = False
        total_num_of_pkts_to_receive_set = False

        while(not end_of_transmission):
            data, address = self.sock.recvfrom(4+CHUNK_SIZE+32)  # 4: seq num; 5: msg size; 32: checksum
            #data = data.decode()
            #print("received", data)
            seq_number = int(data[:4].decode())
            checksum = data[4:4+32].decode()
            msg = data[4+32:]

            if self.checksum_ok(msg, checksum):
                self.sock.sendto((self.num_to_fix_len_string(seq_number)+"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"+"ACK").encode(), address)
                print("ACK sent:", seq_number)

            if seq_number == 0:
                total_num_of_pkts_to_receive = int(msg.decode())
                print("received num of pkts:", total_num_of_pkts_to_receive)
                total_num_of_pkts_to_receive_set = True
            else:
                num_of_pkts_received += 1
                chunks[seq_number] = msg

            if total_num_of_pkts_to_receive_set:
                if total_num_of_pkts_to_receive == num_of_pkts_received:
                    end_of_transmission = True

        return chunks

    def get_chunks_together_in_string(self, chunks):
        chunk_ids = list(chunks.keys())
        result = ''
        for id in chunk_ids:
            result+=(chunks.pop(id).decode())
        # print("result before returning", result)
        return result
