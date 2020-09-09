import serial
import schedule
import time
from time import ctime
import hashlib
from datetime import datetime
import socket
import tqdm
import os
import threading
import json

#block
class Block:
    def __init__ (self, ID=None, transaction=None, prev_hash=None, new_hash=None, timestamp=None):
        self.ID = ID
        self.transaction = transaction
        self.prev_hash = prev_hash
        self.timestamp = timestamp
        self.chain = []
    
    def setID(self):
        if not self.chain:
            self.ID = 1
        else:
            old_id = self.chain[-1][0]
            new_id = old_id + 1
            self.ID = new_id
    
    def setTransaction(self, transaction):
        self.transaction = transaction
    
    def getPrev_hash(self):
        if not self.chain:
            #when chain is empty
            return None
        
        else:
            self.prev_hash = self.chain[-1][3] #index of hash on prev block   

    def setNew_hash(self):
        self.tohash = (str(self.ID) + str(self.transaction) + str(self.prev_hash) + str(self.timestamp))
        self.kelas = "".join(self.tohash)
        self.new_hash = hashlib.sha256(self.kelas.encode('utf-8')).hexdigest()
    
    def setTimestamp(self):
        t = time.time()
        timestamp = ctime(t)
        self.timestamp = timestamp
        
    def printblock(self):
        print("ID = " + str(self.ID) + "\n" + 
        "Jarak = " + str(self.transaction) + "\n" + 
        "Prev_hash = " + str(self.prev_hash) + "\n" + 
        "New_hash = " + str(self.new_hash) + "\n" + 
        "Timestamp = " + str(self.timestamp))
    
    def saveblock(self): #fungsi membuat file .txt
        with open('dist_' + str(self.ID) + '.txt', 'w') as f:
            f.write(str(self.ID) + 
                    "\n" + str(self.transaction) + 
                    "\n" + str(self.prev_hash) + 
                    "\n" + str(self.new_hash) +
                    "\n" + str(self.timestamp))
            f.close()
    
    def last_block(self):
        self.chain[-1]

    def add_block(self):
        item = self.ID, self.transaction, self.prev_hash, self.new_hash, self.timestamp
        ls = list(item)
        self.chain.append(ls)

    def view_chain(self):
        print(self.chain)

    def save_chain(self):
        with open("database.txt", "w") as d:
            d.write(json.dumps(self.chain))

    def clear_chain(self):
        self.chain.clear()

    def open_chain(self): #store chain data from another transaction
        if not self.chain:
            with open('database.txt', 'r') as g:
                b = json.loads(g.read())
                for item in b:
                    self.chain.append(item)
        
        elif self.chain:
            with open('database.txt', 'r') as f:
                a = json.loads(f.read())
                for item in a:
                    for j in range(len(a)):
                        for k in range(4):
                            if a[j][k] == self.chain[j][k]:
                                pass
                            elif a[j][k] != self.chain[j][k]:
                                self.chain.append(item)
        else:
            pass

#Fungsi menghitung data            
def Measure():
    arduino = serial.Serial('/dev/ttyUSB0', 9600)
    sens_in = arduino.readline()
    sensorinput = sens_in.decode().strip("\r\n")
    print(sensorinput)
    
    #Open existing chain
    block.open_chain()
    
    #Giving ID
    block.setID()
    
    #Giving distance value
    block.setTransaction(sensorinput)
    
    #Giving timestamp
    block.setTimestamp()

    #Get prev_hash
    block.getPrev_hash()

    #Giving new_hash
    block.setNew_hash()
    
    #display block
    block.printblock()
    
    #add to chain
    block.add_block()

    #check chain
    block.view_chain()

    #save_chain
    block.save_chain()

    sensorinput = 0    
    arduino.close()
    print("Connection closed...")

#Fungsi pengiriman chain...
def send_chain():
    def ConnectServer1():
        SEPARATOR = "<SEPARATOR>"
        BUFFER_SIZE = 4096 # send 4096 bytes each time step

        # the ip address or hostname of the server, the receiver
        host = "192.168.100.4"
        # the port, let's use 5001
        port = 5001
        # the name of file we want to send, make sure it exists
        filename = fname
        # get the file size
        filesize = os.path.getsize(filename)
        # create the client socket
        s = socket.socket()
        print(f"[+] Connecting to {host}:{port}")
        s.connect((host, port))
        print("[+] Connected.")
        # send the filename and filesize
        s.send(f"{filename}{SEPARATOR}{filesize}".encode())

        # start sending the file
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            for _ in progress:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                # we use sendall to assure transimission in 
                # busy networks
                s.sendall(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))
        # close the socket
        s.close()

    def ConnectServer2():
        SEPARATOR = "<SEPARATOR>"
        BUFFER_SIZE = 4096 # send 4096 bytes each time step

        # the ip address or hostname of the server, the receiver
        host = "192.168.100.5"
        # the port, let's use 5001
        port = 5001
        # the name of file we want to send, make sure it exists
        filename = fname
        # get the file size
        filesize = os.path.getsize(filename)
        # create the client socket
        s = socket.socket()
        print(f"[+] Connecting to {host}:{port}")
        s.connect((host, port))
        print("[+] Connected.")
        # send the filename and filesize
        s.send(f"{filename}{SEPARATOR}{filesize}".encode())

        # start sending the file
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            for _ in progress:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                # we use sendall to assure transimission in 
                # busy networks
                s.sendall(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))
        # close the socket
        s.close()

    def ConnectServer3():
        SEPARATOR = "<SEPARATOR>"
        BUFFER_SIZE = 4096 # send 4096 bytes each time step

        # the ip address or hostname of the server, the receiver
        host = "192.168.100.6"
        # the port, let's use 5001
        port = 5001
        # the name of file we want to send, make sure it exists
        filename = fname
        # get the file size
        filesize = os.path.getsize(filename)
        # create the client socket
        s = socket.socket()
        print(f"[+] Connecting to {host}:{port}")
        s.connect((host, port))
        print("[+] Connected.")
        # send the filename and filesize
        s.send(f"{filename}{SEPARATOR}{filesize}".encode())

        # start sending the file
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            for _ in progress:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                # we use sendall to assure transimission in 
                # busy networks
                s.sendall(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))
        # close the socket
        s.close()

    fname = ("database.txt")

    x = threading.Thread(target=ConnectServer1) #Lubuntu A
    x.start()
    x.join()

    y = threading.Thread(target=ConnectServer2) #Lubuntu B
    y.start()
    y.join()

    z = threading.Thread(target=ConnectServer3) #Lubuntu C
    z.start()
    z.join()

start = input("Do you want to send block? 1. Yes, 2.No \n")
block = Block()

while start == '1':
    print("Creating block...")
    Measure()
    print("Sending block...")
    
    print("Block sent...")
    start = input("Do you wish to continue? 1. Yes, 2. No \n")
