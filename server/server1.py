import socket
import pickle
import threading as thread
from serverdane import *
from time import sleep
import pygame as pg

class ClientThread(thread.Thread):
    def __init__(self, clientsocket, gra, gracz):
        thread.Thread.__init__(self)
        self.clock = pg.time.Clock()
        self.header = 16
        self.client = clientsocket
        self.gra = gra
        print("Połączono z graczem")
        data = b''
        new_msg = True
        while True:
            msg = self.client.recv(2048)
            if new_msg:
                msglen = int(msg[:self.header])
                new_msg = False
            data += msg
            if len(data) - self.header == msglen:
                break
        self.identity = pickle.loads(data[self.header:])
        self.gracz = gracz
        if len(self.gra.players) > 0:
            for player in self.gra.players:
                if player.name == self.identity:
                    self.gracz = player.id
                    self.gra.players[self.gracz].aktywny = True
            if not any(player.name == self.identity for player in self.gra.players):
                self.gra.players.append(Player(1, 1, self.gracz, self.identity))
                self.gra.players[self.gracz].aktywny = True
        else:
            self.gra.players.append(Player(1, 1, self.gracz, self.identity))
            self.gra.players[self.gracz].aktywny = True


    def run(self):
        self.all = self.gra.walls + self.gra.players + self.gra.potwory + self.gra.skarby + self.gra.przejscie
        self.all_msg = pickle.dumps(self.all)
        print("Mapa wysyłana")
        self.client.sendall(bytes(f"{len(self.all_msg):<{self.header}}", 'utf-8') + self.all_msg)
        print("Mapa wysłana")
        reply = ""
        while self.client:
            self.events()
            self.update()

    def events(self):
        data = b''
        new_msg = True
        while True:
            msg = self.client.recv(2048)
            if new_msg:
                msglen = int(msg[:self.header])
                new_msg = False
            data += msg
            if len(data) - self.header == msglen:
                break
        event = pickle.loads(data[self.header:])
        if not self.gra.players[self.gracz].walka:
            if event == pg.K_LEFT or event == pg.K_a:
                if self.gra.players[self.gracz].przejscie(self.gra.przejscie, dx = -1):
                    self.gra.players[self.gracz].set_pos(1, 1)
                    self.gra.players[self.gracz].aktywny = False
                    msg = pickle.dumps(["przejscie"])
                    self.client.sendall(bytes(f"{len(msg):<{self.header}}", 'utf-8') + msg)
                else:
                    self.gra.players[self.gracz].move(self.gra.walls, self.gra.skarby, self.gra.potwory, dx=-1)
            if event == pg.K_UP or event == pg.K_w:
                if self.gra.players[self.gracz].przejscie(self.gra.przejscie, dy = -1):
                    self.gra.players[self.gracz].set_pos(1, 1)
                    self.gra.players[self.gracz].aktywny = False
                    msg = pickle.dumps(["przejscie"])
                    self.client.sendall(bytes(f"{len(msg):<{self.header}}", 'utf-8') + msg)
                else:
                    self.gra.players[self.gracz].move(self.gra.walls, self.gra.skarby, self.gra. potwory, dy=-1)
            if event == pg.K_RIGHT or event == pg.K_d:
                if self.gra.players[self.gracz].przejscie(self.gra.przejscie, dx = 1):
                    self.gra.players[self.gracz].set_pos(1, 1)
                    self.gra.players[self.gracz].aktywny = False
                    msg = pickle.dumps(["przejscie"])
                    self.client.sendall(bytes(f"{len(msg):<{self.header}}", 'utf-8') + msg)
                else:
                    self.gra.players[self.gracz].move(self.gra.walls, self.gra.skarby, self.gra.potwory, dx=1)
            if event == pg.K_DOWN or event == pg.K_s:
                if self.gra.players[self.gracz].przejscie(self.gra.przejscie, dy = 1):
                    self.gra.players[self.gracz].set_pos(1, 1)
                    self.gra.players[self.gracz].aktywny = False
                    msg = pickle.dumps(["przejscie"])
                    self.client.sendall(bytes(f"{len(msg):<{self.header}}", 'utf-8') + msg)
                else:
                    self.gra.players[self.gracz].move(self.gra.walls, self.gra.skarby, self.gra.potwory, dy=1)
            if isinstance(event, Uzbrojenie):
                for ekwipunek in self.gra.players[self.gracz].ekwipunek:
                    if event.id == ekwipunek.id:
                        self.gra.players[self.gracz].zaloz_eq(ekwipunek)
        if self.gra.players[self.gracz].walka:
            if event == pg.K_1:
                self.gra.players[self.gracz].battle.atak_zwykly()
            if event == pg.K_2:
                self.gra.players[self.gracz].battle.heal()
            if event == pg.K_3:
                self.gra.players[self.gracz].battle.mp_regen()
            if event == pg.K_4:
                self.gra.players[self.gracz].battle.atak_precyzyjny()
            if event == pg.K_5:
                self.gra.players[self.gracz].battle.atak_potezny()


    def update(self):
        state = self.gra.players + self.gra.potwory + self.gra.skarby
        print("Wysyłam update")
        update_msg = pickle.dumps(state)
        self.client.sendall(bytes(f"{len(update_msg):<{self.header}}", 'utf-8') + update_msg)


class serverThread(thread.Thread):
    def __init__(self, gra):
        thread.Thread.__init__(self)
        self.gra = gra
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv.connect(("127.0.0.1",9005))
        print("Połączono")
        self.header = 16

    def run(self):
        while self.serv:
            sleep(2)
            self.receivePlayers()
            self.sendPlayers()
            print("Gracze zaktualizowani")

    def sendPlayers(self):
        players = []
        if len(self.gra.players) > 0:
            for player in self.gra.players:
                if player.aktywny:
                    players.append(player)
        players_update = pickle.dumps(players)
        self.serv.sendall(bytes(f"{len(players_update):<{self.header}}", 'utf-8') + players_update)

    def receivePlayers(self):
        data = b''
        new_msg = True
        while True:
            msg = self.serv.recv(2048)
            if new_msg:
                msglen = int(msg[:self.header])
                new_msg = False
            data += msg
            if len(data) - self.header == msglen:
                break
        players = pickle.loads(data[self.header:])
        for player in players:
            if player.aktywny and any(gracz.name == player.name for gracz in self.gra.players):
                for gracz in self.gra.players:
                    if gracz.name == player.name:
                        gracz.update(player)
            if not any(gracz.name == player.name for gracz in self.gra.players):
                self.gra.players.append(Player(1, 1, len(self.gra.players), player.name))

class Gameserver:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.walls = []
        self.players = []
        self.potwory = []
        self.skarby = []
        self.przejscie =[]
        self.load("mapa1.txt")
        try:
            self.s.bind(('127.0.0.1', 9010))
        except socket.error as e:
            print(str(e))
        self.s.listen(2)

    def load(self, mapa):
        self.mapa = []
        raw = open(mapa, "r")
        for line in raw:
            self.mapa.append(line)
        for row, tiles in enumerate(self.mapa):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    self.walls.append(Wall(col, row))
                if tile == 'x':
                    self.potwory.append(Potwor(col,row, len(self.potwory)))
                if tile == 's':
                    self.skarby.append(Skarb(col, row, str(len(self.skarby))+"s2"))
                if tile == "o":
                    self.przejscie.append(Przejscie(col, row))
        print("Mapa załadowana")

    def run(self):
        servthread = serverThread(self)
        servthread.start()
        while True:
            conn, addr = self.s.accept()
            newthread = ClientThread(conn, self, len(self.players))
            newthread.start()

server = Gameserver()
server.run()