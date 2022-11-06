import socket
import time
import os
import hashlib
from typing import BinaryIO


def md5(f: BinaryIO):
    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: f.read(4096), b""):
        hash_md5.update(chunk)
    return hash_md5.hexdigest()


server_ip_addr = '47.100.6.196'
server_port = 7070
BACKLOG = 5
file_path = r'D:\Codes\Python\DevNetZhangXiang\socket\files'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', server_port))
s.listen(BACKLOG)
while True:  # 每十秒重新尝试连接一次
    try:
        conn, addr = s.accept()
        print(f'{time.time()}:connect success')



        continue
    except Exception as e:
        print(f'connect error:{e}')
    finally:
        time.sleep(10)
        continue

while True:
    try:
        filename = str(s.recv(1024))
        data = total_data = s.recv(1024)
        while len(data) > 0:
            data = s.recv(1024)
            total_data += data

        with open(os.path.join(file_path, filename), "wb+") as f:
            f.write(total_data)
            s.sendall(md5(f))
    except Exception as e:
        print(f'transition error:{e}')
    finally:
        s.sendall("-1")
        continue
