import socket
import hashlib

class Receiver:
    def __init__(self, server_address, chunk_size):
        self.server_address = server_address
        self.chunk_size = chunk_size

    # PRE: binded socket
    def receive_message(self, socket, filename, msg_type):
        """
        msg_type: specify whether you're receiving a command ("CMD") or the
        body of a msg ("BDY"). This serves the purpose to detect the correct
        end of transmission.
        """
        chunks = self.receive(socket, msg_type)
        return self.get_chunks_together(chunks, filename)

    def num_to_fix_len_string(self, num):
        return str(num).zfill(4)

    def get_chunks_together(self, chunks, filename):
        chunk_ids = list(chunks.keys())
        with open(filename, 'wb') as file:
            for id in chunk_ids:
                file.write(chunks.pop(id))
                # msg += chunks.pop(id)
        file.close()
        # return msg

    def checksum_ok(self, msg, checksum):
        return hashlib.md5(msg).hexdigest() == checksum

    def recieve_string(self, socket, msg_type):
        """
        msg_type: specify whether you're receiving a command ("CMD") or the
        body of a msg ("BDY"). This serves the purpose to detect the correct
        end of transmission.
        """
        return self.get_chunks_together_in_string(self.receive(socket, msg_type))

    # PRE: binded socket
    def receive(self, socket, msg_type):
        self.sock = socket  
        
        chunks = {}     # K: seq_num; V: chunk data

        end_of_transmission = False
        while(not end_of_transmission):
            data, address = self.sock.recvfrom(4+self.chunk_size+32)  # 4: seq num; 5: msg size; 32: checksum
            #data = data.decode()
            #print("received", data)
            seq_number = int(data[:4].decode())
            checksum = data[4:4+32].decode()
            msg = data[4+32:]

            if(self.checksum_ok(msg, checksum)):
                self.sock.sendto(("ACK" + self.num_to_fix_len_string(seq_number)).encode(), address)
                print("ACK sent:", seq_number)

            if(seq_number == 0):
                if(msg == msg_type):
                    print("received eot")
                    end_of_transmission = True
                break
            chunks[seq_number] = msg

        return (chunks)
      

    def get_chunks_together_in_string(self, chunks):
        print('getting things together; chunks:', chunks)
        chunk_ids = list(chunks.keys())
        result = ''
        for id in chunk_ids:
            result+=(chunks.pop(id).decode())
                # msg += chunks.pop(id)
        print("result before returning", result)
        return result
        #return msg

