import socket
from random import randint
import os
from termios import tcflush, TCIFLUSH
import time, sys


def debug(text):
    print "======"
    print text
    print "======"



class Client():
    def __init__(self):
        self.socket = socket.socket()
        self.name = ""
        self.SCORE = {}
        self.LNUM = 0
        self.PNUM = 0

    def connectServer(self, host, port):
        # CONNECT
        self.socket.connect((host,port))
        #Receive server information
        info = self.socket.recv(1024).decode()
        print("Current server: " + info.split(" ")[0] + "/" + info.split(" ")[1])
        self.PNUM = int(info.split(" ")[1])
        # SETUP NAME
        print("Input user name: ")
        while True:
            name = raw_input()
            self.socket.send(name.encode())
            res = self.socket.recv(1024).decode()
            if res == "e0":
                print( "Syntax error")
            elif res == "e1":
                print( "Username is used")
            else:
                print( "Registered to server")
                self.name = name
                self.LNUM = int(res)
                break
            print( "Please choose other username: ")
        #Wait for others player
        while True:
            count = self.socket.recv(1024).decode()
            print((str(count) + "/" + str(self.PNUM) + "player connected to server"))
            if (int(count) == self.PNUM):
                print("All players connected. Game will start in 3s")
                break


    def printScore(self):
         for player in self.SCORE:
            space = ""
            for i in range(0,20 - len(player)):
                space += " "
            print(str(player) + space + str(self.SCORE[player]))

    def initGame(self):
        os.system("clear")
        list_player = self.socket.recv(1024)
        for player in list_player.split():
            self.SCORE[player] = 0
        self.printScore()


    def startGame(self):
        while True:
            #Nhan ten player den luot tu server
            player = self.socket.recv(1024).decode()
            print(str(player) + "'s turn ...")
            if (player == self.name):
                #Neu la luot minh
                while True:
                    print "Your turn, type roll to roll ..."
                    #Bug here, need to clear buffer
                    tcflush(sys.stdin, TCIFLUSH)
                    text = raw_input()
                    if text == "roll":
                        break
                roll = randint(1,6)
                print ("You rolled " + str(roll) + " point" )
                self.socket.send(str(roll).encode())
            new_score = self.socket.recv(1024).decode()
            if (new_score == "win"):
                print ("Player " + player + " won")
                print ("The game will end in 3s ...")
                self.socket.close()
                exit()
            else:
                self.SCORE[player] = int(new_score)            
            time.sleep(1)
            os.system("clear")
            self.printScore()
            print "======================="
            print "Next turn"


fClient = Client()
fClient.connectServer(socket.gethostname(),12345)
fClient.initGame()
fClient.startGame()
        