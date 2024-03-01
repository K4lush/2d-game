import socket
import pickle

import json

from Settings import Settings

class Network:
    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Change to UDP

        # self.server = "172.20.10.12"
        # self.port = 12345
        self.server = ip
        self.port = port
        self.addr = (self.server, self.port)
        self.connect = self.connect()

    def connect(self):
        try:
            #print(self.addr)
            self.client.connect(self.addr)
        except pickle.UnpicklingError as pe:
            print(f"Pickle Unpickling Error: {pe}")
        except Exception as e:
            print(f"General Connection Error: {e}")
        return None

    # def send(self, data):
    #     """
    #     Send data to the server.
    #     """
    #     try:
    #         self.client.send(pickle.dumps(data))
    #     except socket.error as e:
    #         print(e)

    def send(self, data):
        try:
            json_data = json.dumps(data)

            self.client.sendall(json_data.encode())  # Send the JSON string directly

            #print("NETWORK: Sending data...", data)

        except socket.error as e:
            print(e)

    # def receive(self):
    #     try:
    #         buffer_size = 4096
    #         json_data = self.client.recv(buffer_size).decode('utf-8')  # Receive bytes, decode to string
    #
    #         print("NETWORK: Receiving data after decoding...", json_data)
    #
    #         data = json.loads(json_data)  # Convert JSON string to Python data
    #
    #         # print("NETWORK: Receiving data after loading...", data)
    #
    #         return data
    #     except socket.error as e:
    #         print(f"Socket Error: {e}")
    #     except Exception as e:
    #         print(f"General Error: {e}")
    #     return None

    def receive(self):
        try:
            buffer_size = 4096
            received_data = self.client.recv(buffer_size).decode('utf-8')  # Receive the raw data
            #print("NETWORK: Raw Data Received:", received_data)  # Inspect this!

            # json_data = received_data.decode('utf-8')

            data = json.loads(received_data)

            #print("NETWORK: Data Received:", received_data)  # Inspect this!


            return data
        except socket.error as e:
            print(f"Socket Error: {e}")
        except Exception as e:
            print(f"General Error: {e}")
        return None