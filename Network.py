import socket
import pickle

class Network:
    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server = "172.20.10.12"
        # self.port = 12345
        self.server = ip
        self.port = port
        self.addr = (self.server, self.port)
        self.connect = self.connect()

    def connect(self):
        try:
            print(self.addr)
            self.client.connect(self.addr)
        except pickle.UnpicklingError as pe:
            print(f"Pickle Unpickling Error: {pe}")
        except Exception as e:
            print(f"General Connection Error: {e}")
        return None

    def send(self, data):
        """
        Send data to the server.
        """
        try:
            self.client.send(pickle.dumps(data))
        except socket.error as e:
            print(e)

    def receive(self):
        """
        Receive data from the server.
        """
        try:
            # Adjust the buffer size as needed
            buffer_size = 4096
            received_data = self.client.recv(buffer_size)
            #print(pickle.loads(received_data))
            return received_data  # Return the raw data
        except socket.error as e:
            print(f"Socket Error: {e}")
        except Exception as e:
            print(f"General Error: {e}")
        return None