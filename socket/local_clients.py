import json
import socket
import os
import hashlib
import time
from io import BytesIO
from typing import BinaryIO

import requests


def md5(f: BinaryIO):
    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: f.read(4096), b""):
        hash_md5.update(chunk)
    return hash_md5.hexdigest()


server_ip_addr = '47.109.48.16'
server_port = 9090
file_path = r'D:\Codes\Python\DevNetZhangXiang\socket\files'
md5_url = "http://47.109.48.16:9090/file/syn/md5/"

while True:
    syn_get_url = "http://47.109.48.16:9090/file/syn/0"
    syn_res = requests.get(syn_get_url)
    syn_list = syn_res.json()['data']
    for syn in syn_list:
        file_url = syn['url']
        file_res = requests.get(file_url)
        with BytesIO(file_res.content) as remote:
            with open(os.path.join(file_path, syn['name']), "wb+") as local:
                local.write(remote.read())
                local.flush()
                local.close()
                with open(os.path.join(file_path, syn['name']), "rb+") as f:
                    test_md5 = md5(f)
                    print(md5_url + test_md5)
                    requests.get(md5_url + test_md5)
                    f.close()
                print("get file" + syn['name'])
    print('等待下一次连接', end='')
    for i in range(10):
        time.sleep(1)
        print('.', end='')
    print()
