#-*- coding : utf-8-*-
# coding:unicode_escape
'''
    DATE: 2023-02-24
    AUTHER: Nexus
'''

import socket
import largePrime
import os
import random
import tqdm
from Crypto.Cipher import AES
from urllib import parse # 针对中文解码的库
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5004

BUFFER_SIZE = 1024*1024*2
SEPARATOR = "<SEPARATOR>"

# 建立 TCP 连接
s = socket.socket()
s.bind((SERVER_HOST,SERVER_PORT))
# 10 -> 最大允许连接数
s.listen(10)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

# 允许连接
client_socket, address = s.accept() 
print(f"[+] {address} is connected.")

# 开始DH密钥交换
recv_q = client_socket.recv(BUFFER_SIZE).decode()
print("Server recv q = ",recv_q)
recv_q = (int)(recv_q)

# 生成元
recv_g = client_socket.recv(BUFFER_SIZE).decode()
print("Server recv g = ",recv_g)
recv_g = (int)(recv_g)

# 对方的a
recv_a = client_socket.recv(BUFFER_SIZE).decode()
print("Server recv a = ",recv_a)
recv_a = (int)(recv_a)

# 自己的b
server_send_b = (str)( random.randint(100,1024) )
print("server_send_b = ",server_send_b)
client_socket.send(server_send_b.encode('utf-8'))
# 成功发送
server_send_b = (int)(server_send_b)
Y_b = pow(recv_g,server_send_b,int(recv_q))
print("Y_b = ",Y_b)
Y_b = (str)(Y_b)
client_socket.send(Y_b.encode('utf-8'))
# 测试√

Y_a = client_socket.recv(BUFFER_SIZE).decode()
K_b = pow((int)(Y_a),(int)(server_send_b),(int)(recv_q))
print("Y_a = ",Y_a)
print("K_b = ",K_b)
# 测试√ K_a = K_b,密钥分配完成

de_key = client_socket.recv(BUFFER_SIZE).decode('ISO-8859-1')
print("dekey => ",de_key)
de_key = de_key.encode('ISO--8859-1') # --> bytes
aes = AES.new(de_key,AES.MODE_ECB)

received = client_socket.recv(BUFFER_SIZE).decode('ISO-8859-1')
filename, filesize = received.split(SEPARATOR)
# 若有路径名,则去除路径
filename = os.path.basename(filename)
# int强转
filesize = int(filesize)

# 接收并写文件
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "w",encoding='utf-8') as f:
    while True:
        # read 1024 bytes from the socket (receive)
        bytes_read_crypted = client_socket.recv(BUFFER_SIZE)
        bytes_read = aes.decrypt(bytes_read_crypted)
        ans_for_bar = aes.decrypt(bytes_read_crypted)        
        bytes_read = bytes_read.decode('utf-8')
        
        if not bytes_read_crypted:    
            break
        # print("bytes_read_crypted",bytes_read_crypted)
        # print("bytes_read_r",bytes_read_r)
        # print("bytes_read",bytes_read)
        # f.write(bytes_read )
        res = bytes_read
        ans = bytes_read.encode()
        # print("bytes_read_str =  ",bytes_read[2:-1])
        # 取两个 ’ 之间的内容
        start_position = bytes_read.find("'",1)
        end_position = bytes_read.find("'",2)
        # print("start_position = ",start_position)
        # print("end_position = ",end_position)
        res = res[(start_position+1):end_position]
        # print(" res = ",res)
        # 上面是 去掉 b 和两个 ’ 符号
        # 转为bytes    
        res = res.encode('unicode_escape')
        # print(" res_1 = ",res)
        res2 = res.decode('utf-8').replace(r'\\\\x','%')
        # print(" res_2 = ",res2)
        res3 = parse.unquote(res2)
        res3 = res3.replace(r'\\\\r\\\\n','\\r\\n')
        # 把 \\r和\\n 转换为真正的回车换行，否则会显示 \r\n 
        print(" res = ",res3)
        # 上面针对中文字符做了 replace 和 unqote 处理
        f.write(res3)
        progress.update(filesize)

# close the client socket
client_socket.close()
# close the server socket
s.close()

