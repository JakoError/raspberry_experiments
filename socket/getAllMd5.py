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


file_path = r'D:\Codes\Python\DevNetZhangXiang\socket\files'
for file in os.listdir(file_path):
    with open(os.path.join(file_path, file), "rb") as f:
        print(f"{file} {md5(f)}")

print(bytes('0\0', encoding='utf-8'))
