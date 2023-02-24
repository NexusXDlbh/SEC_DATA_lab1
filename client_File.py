#-*- coding : utf-8-*-
'''
    DATE: 2023-02-24
    AUTHER: Nexus
'''
import tqdm
import os
import socket
import largePrime
import random
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

# 1. Preparation
# separate the data fields
SEPARATOR = "<SEPARATOR>" 

# send 4096 bytes each time step
BUFFER_SIZE = 1024*1024*2 

# the ip address or hostname of the server, the receiver
host = "127.0.0.1"

# the port, let's use 5002
port = 5004

# the name of file we want to send, make sure it exists
filename = "test.txt"

# get the file size in bytes, as we need it to show process bars
filesize = os.path.getsize(filename)

# 2.TCP Connection
# create the client socket
s = socket.socket()

# connecting to the server
print(f"[+] Connecting to {host}:{port}")
s.connect((host,port))
print(f"[+] Connected.")

# DH-generate large prime
q = (str) (largePrime.getLargePrime(256))
# print('large_prime= \n ' + (str)(q))
# q 测试 √

s.send(q.encode('utf-8'))

# DH-generate g (生成元)
g = (str) ( largePrime.getGenerator(6) )
print("g=",g) 
s.send(g.encode('utf-8'))
g = (int) (g)
# g 测试 √

a = (str)(random.randint(100,1024))
print("a=",a)
s.send(a.encode('utf-8'))
a = (int) (a)

b = s.recv(BUFFER_SIZE).decode()
b = (int) (b)
print("Client recv b=",b)

Y_a = pow(g,a,int(q))
print("Y_a = ",Y_a)
Y_a = (str)(Y_a)
s.send(Y_a.encode('utf-8'))
# Y_a 测试 √

Y_b = s.recv(BUFFER_SIZE).decode()
print("Client recv Y_b=",Y_b)
# 测试√
K_a = pow((int)(Y_b),(int)(a),(int)(q))
print("K_a = ",K_a)
K_a = (str)(K_a)
# 测试√ K_a = K_b,密钥分配完成

key = K_a[1:33]
print("key => " , key)
s.send(key.encode('ISO-8859-1'))
key = key.encode('ISO--8859-1')
#c send the filename and filesize
# enode() function encodes the string we passed
# to 'utf-8' encoding (that's necessary)
s.send(f"{filename}{SEPARATOR}{filesize}".encode('ISO-8859-1'))

def add_2_16(value):
    length = len(value)
    count = length
    
    while(count % 16 != 0):
        value += '0'
        count += 1 
    
    return value

aes = AES.new(key,AES.MODE_ECB)
#cipher = AES.new(key)
# 3.start sending the file
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)

with open(filename, "rb") as f: # "rb" read in binary 
    while True:
        # read the bytes from the file
        bytes_read_f = f.read(BUFFER_SIZE)        
        if not bytes_read_f:
            break
        bytes_read_2str = str(bytes_read_f) 
        bytes_read_2str = add_2_16(bytes_read_2str)
        bytes_read_o = aes.encrypt(bytes_read_2str.encode('ISO-8859-1'))
        #bytes_read = b2a_hex(bytes_read_o)
        print(" byte_before_crypted => ",bytes_read_f)
        print(" byte_read_crypted => ",bytes_read_o)
        
        s.sendall(bytes_read_o)
        progress.update(len(bytes_read_f))
        

# 4.close the socket
s.close()