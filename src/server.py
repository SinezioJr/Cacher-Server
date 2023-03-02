from socket import *
import os

from _thread import *
import threading

import sys

PORT = int(sys.argv[1])
DIR = sys.argv[2]

BUFFER_SIZE = 4*1024
SEPARATOR = "<SEPARATOR>"
MAX_CACHE_SIZE = 64 * 1048576

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', PORT))
serverSocket.listen(1)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

print("The server is ready to receive on port {0}".format(PORT))

lock = threading.Lock()


class CacheModel:
    data = {}
    dataSize = {}
    totalSize = 0

    def findoncache(self, fn, fileSize):
        if (fn in self.data):
            print(f"Cache hit. File {fn} sent to the client.")
            return self.data[fn]["file"]
        else:
            print(f"Cache miss. File {fn} sent to the client")
            self.addToCache(fn, fileSize)
            return None

    def addToCache(self, fn, fileSize):
        new_data = {"file": open(fn, 'rb'), "size": fileSize, }
        if (fileSize < MAX_CACHE_SIZE):
            if ((self.totalSize+fileSize) < MAX_CACHE_SIZE):
                self.data[fn] = new_data
            else:
                if (self.clearCache(fileSize)):
                    self.data[fn] = new_data
            self.totalSize += fileSize

    def clearCache(self, fileSize):
        while (MAX_CACHE_SIZE-self.totalSize < fileSize):
            min_val = max(self.data.items(), key=lambda x: x[1]["size"])
            lock.acquire()

            try:
                self.totalSize -= min_val[1]["size"]
                self.data.pop(min_val[0])
            finally:
                lock.release()

        return True


def requestProcess(connectionSocket, addr):
    sentence = connectionSocket.recv(BUFFER_SIZE)

    if (sentence.decode("utf-16") == "list"):
        connectionSocket.send(("list of files:\n - " +
                              "\n - ".join(os.listdir(DIR))).encode("utf-16"))
        connectionSocket.close()
        return 1

    filename = f"{DIR}/{sentence.decode('utf-16')}"

    print(f"\nClient {addr} is requesting file {filename}")

    try:
        filesize = os.path.getsize(filename)
        response = str(filesize).encode("utf-16")
        connectionSocket.send(response)

        checkCache = cache.findoncache(filename, filesize)
        file = checkCache if checkCache else open(filename, "rb")

        if checkCache:
            lock.acquire()

        while True:
            bytes_read = file.read(BUFFER_SIZE)
            if not bytes_read:
                break
            connectionSocket.sendall(bytes_read)

    except FileNotFoundError:
        print("erro: file not found")
        response = 'HTTP/1.0 404 NOT FOUND\n\File Not Found'
        connectionSocket.send(response)
    finally:
        if checkCache:
            lock.release()

    connectionSocket.close()
    return 1


cache = CacheModel()

while True:
    connectionSocket, addr = serverSocket.accept()

    start_new_thread(requestProcess, (connectionSocket, addr[0]))

s.close()
