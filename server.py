import socket
import Tkinter as tk
import re
import threading
import time


#Check name function, return: 0 (fail <syntax error>), 1 (success), 2 (fail <name is used>)
def checkName(name):
    pattern = re.compile("([^a-zA-Z0-9])+")
    if (pattern.search(name) != None):
        return 0
    if (len(name) > 10):
        return 0
    if (name in CONNECTION):
        return 2
    return 1

class setUpConnectionThread(threading.Thread):
    def __init__(self, connect):
        threading.Thread.__init__(self)
        self.connect = connect
    def run(self):
        global CONNECTION
        while True:
            name = self.connect.recv(1024)
            if (checkName(name) == 1):
                self.connect.send("1")
                CONNECTION[name] = []
                CONNECTION[name].append(connect)
                print ("Player " + name + " connected")
                break
            elif checkName(name) == 0:
                self.connect.send("0")
            else:
                self.connect.send("2")

class countPlayerThread(threading.Thread):
    def __init__(self, CONNECTION):
        threading.Thread.__init__(self)
        self.PCount = 0
        self.CONNECTION = CONNECTION

    def run(self):
        while True:
            time.sleep(1)
            global CONNECTION
            if (len(CONNECTION) != self.PCount):
                for name in CONNECTION:
                    CONNECTION[name][0].send(str(len(CONNECTION)))
                self.PCount = len(CONNECTION)
                if (self.PCount == PNUM):
                    for name in CONNECTION:
                        CONNECTION[name][0].send("Done")
                    return


class Server():
    def __init__(self, host, port, PNUM):
        self.socket = socket.socket()
        self.socket.bind((host,port))
        self.PNUM = PNUM
        self.CONNECTION = {}
        self.countPThred = countPlayerThread()
    
    def openForConnection(self):
        self.socket.listen(5)
        print "Waiting for player to connect ..."
        self.countPThred.start()
        while (len(self.CONNECTION) < self.PNUM):
            connect, addr = self.socket.accept()
            setupThread = setUpConnectionThread(connect)
            setupThread.start()