from socket import *
import tqdm

import os
import sys

HOST = sys.argv[1]
PORT = int(sys.argv[2])

DIR = sys.argv[3]

BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"


def requestFile(filename):
    s = socket()
    print(f"[+] Connecting to {HOST}:{PORT}")
    s.connect((HOST, PORT))
    print("[+] Connected.")

    s.send(filename.encode())
    filesize = s.recv(BUFFER_SIZE).decode()
    print("filesize: ", filesize)
    filesize = int(filesize)
    progress = tqdm.tqdm(range(
        filesize), f"Saving {filename}", unit="B", unit_scale=True, unit_divisor=1024)

    with open(f"{DIR}/{filename}", "wb") as f:
        while True:
            bytes_read = s.recv(BUFFER_SIZE)
            if not bytes_read:
                break
            f.write(bytes_read)
            progress.update(len(bytes_read))

    os.remove(f"{DIR}/{filename}")


requestFile("file4.txt")
requestFile("file4.txt")
requestFile("file3.txt")

# requestFile("file3.txt")
