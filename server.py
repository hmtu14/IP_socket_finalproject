import socket
# import Tkinter as tk
import re
import threading
import time


#Check name function, return: 0 (fail <syntax error>), 1 (success), 2 (fail <name is used>)


# class setUpConnectionThread(threading.Thread):
#     def __init__(self, connect):
#         threading.Thread.__init__(self)
#         self.connect = connect
#     def run(self):
#         global CONNECTION
#         while True:
#             name = self.connect.recv(1024)
#             if (checkName(name) == 1):
#                 self.connect.send("1".encode())
#                 CONNECTION[name] = []
#                 CONNECTION[name].append(connect)
#                 print ("Player " + name + " connected")
#                 break
#             elif checkName(name) == 0:
#                 self.connect.send("0".encode())
#             else:
#                 self.connect.send("2".encode())

# class countPlayerThread(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#         self.PCount = 0

#     def run(self):
#         while True:
#             time.sleep(1)
#             if (len(self.CONNECTION) != self.PCount):
#                 for name in self.CONNECTION:
#                     self.CONNECTION[name][0].send(str(len(self.CONNECTION)).encode())
#                 self.PCount = len(self.CONNECTION)
#                 if (self.PCount == self.PNUM):
#                     for name in self.CONNECTION:
#                         self.CONNECTION[name][0].send("Done".encode())
#                     return


class Server():

    def checkName(self, name):
            pattern = re.compile("([^a-zA-Z0-9])+")
            if (pattern.search(name) != None):
                return 0
            if (len(name) > 10):
                return 0
            if (name in self.CONNECTION):
                return 2
            return 1

    class countPlayerThread(threading.Thread):
        def __init__(self, server):
            threading.Thread.__init__(self)
            self.PCount = 0
            self.Server = server

        def run(self):
            while True:
                if (len(self.Server.CONNECTION) != self.PCount):
                    for name in self.Server.CONNECTION:
                        self.Server.CONNECTION[name][0].send(str(len(self.Server.CONNECTION)).encode())
                    self.PCount = len(self.Server.CONNECTION)
                    if (self.PCount == self.Server.PNUM):
                        for name in self.Server.CONNECTION:
                            self.Server.CONNECTION[name][0].send("Done".encode())
                        self.Server.socket.close()
                        return

    class setUpConnectionThread(threading.Thread):

        def __init__(self, server, connect):
            threading.Thread.__init__(self)
            self.connect = connect
            self.Server = server
            
        def run(self):
            # Sent server information (Current number of player and Max number of player)
            time.sleep(1)
            self.connect.send((str((len(self.Server.CONNECTION))) + " " + str(self.Server.PNUM)).encode())
            #Wait for player to register
            while True:
                name = self.connect.recv(1024).decode()
                if (self.Server.checkName(name) == 1):
                    self.connect.send("1".encode())
                    self.Server.CONNECTION[name] = []
                    self.Server.CONNECTION[name].append(self.connect)
                    print ("Player " + name + " connected")
                    break
                elif self.Server.checkName(name) == 0:
                    self.connect.send("0".encode())
                else:
                    self.connect.send("2".encode())


    def __init__(self, host, port, PNUM):
        self.socket = socket.socket()
        self.socket.bind((host, port))
        self.PNUM = PNUM
        self.CONNECTION = {}
        self.countPThred = Server.countPlayerThread(self)
        self.countPThred.start()
        self.connectLock = False
        print("Created server")
    
    def openForConnection(self):
        self.socket.listen(5)
        print ("Waiting for player to connect ...")
        while (len(self.CONNECTION) < self.PNUM):
            try:
                connect, addr = self.socket.accept()
                setupThread = Server.setUpConnectionThread(self, connect)
                setupThread.start()
            except:
                print("All players connected. Game will start in 3s")

    def initGame(self):
        print("List of player: ")
        for player in self.CONNECTION:
            print(player)

fServer = Server(socket.gethostname(),1234,3)
fServer.openForConnection()
fServer.initGame()