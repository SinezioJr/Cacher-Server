from socket import *
import tqdm

import sys

HOST = sys.argv[1]
PORT = int(sys.argv[2])

filename = sys.argv[3]
DIR = ""

if len(sys.argv) >= 5:
    DIR = sys.argv[4]

BUFFER_SIZE = 4*1024
SEPARATOR = "<SEPARATOR>"

s = socket()

s.connect((HOST, PORT))

s.send(filename.encode("utf-16"))
response = s.recv(BUFFER_SIZE)

if (filename == "list"):
    print(response.decode("utf-16"))
    exit(1)

filesize = response.decode("utf-16")
filesize = int(filesize.replace('\x00', ''))

progress = tqdm.tqdm(range(
    filesize), f"Saving {filename}", unit="B", unit_scale=True, unit_divisor=1024)

with open(f"{DIR}/{filename}", "wb") as f:
    while True:
        bytes_read = s.recv(BUFFER_SIZE)
        if not bytes_read:
            break
        f.write(bytes_read)
        progress.update(len(bytes_read))

s.close
