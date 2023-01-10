import socket
import pickle
import sys
import pygame as pg
import serverdane as sd
from clientdane import *
from config import *

class Gra:
    def __init__(self):
        self.add_name()
        pg.init()
        self.screen = pg.display.set_mode((szer, wys))
        pg.display.set_caption("Gra")
        self.port = port
        self.instrukcja = None
        self.lista = None
        self.deathscreen = None
        self.button_eq = pg.Rect(171, 384, 171, 64)
        self.button_lista = pg.Rect(341, 384, 171, 64)
        self.button_instr = pg.Rect(0, 384, 171, 64)
        self.image_eq = pg.image.load("Sprites/button_ek.png")
        self.image_lista = pg.image.load("Sprites/button_lis.png")
        self.image_instr = pg.image.load("Sprites/button_instr.png")
        self.all_sprites = pg.sprite.Group()
        self.create_ground()
        self.header = 16
        self.create_socket(server, port)
        self.load_map()

    def run(self):
        self.running = True
        while self.running:
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()
        self.draw()

    def draw_grid(self):
        for x in range(0, szer, tile):
            pg.draw.line(self.screen, (100, 100, 100), (x, 0), (x, wys))
        for y in range(0, wys, tile):
            pg.draw.line(self.screen, (100, 100, 100), (0, y), (szer, y))

    def draw(self):
        self.screen.fill((40, 40, 40))
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.image_instr, (0,384))
        self.screen.blit(self.image_eq, (171,384))
        self.screen.blit(self.image_lista, (341,384))
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN and not self.deathscreen:
                if not self.player.eq_screen_active and not self.lista and not self.instrukcja:
                    msg = pickle.dumps(event.key)
                    self.s.send(bytes(f"{len(msg):<{self.header}}", 'utf-8') + msg)
                    self.player_update()
                if event.key == pg.K_i:
                    self.player.otworz_eq()
                if event.key == pg.K_h:
                    if not self.instrukcja:
                        self.instrukcja = Instrukcja(self)
                    else:
                        self.instrukcja.remove_sprite()
                        self.instrukcja = None
                if event.key == pg.K_o:
                    if not self.lista:
                        self.lista = Lista(self)
                    else:
                        self.lista.remove_sprite()
                        self.lista = None
            if event.type == pg.MOUSEBUTTONDOWN and not self.deathscreen:
                if self.button_eq.collidepoint(event.pos) and event.button == 1:
                    self.player.otworz_eq()
                if self.button_instr.collidepoint(event.pos) and event.button == 1:
                    if not self.instrukcja:
                        self.instrukcja = Instrukcja(self)
                    else:
                        self.instrukcja.remove_sprite()
                        self.instrukcja = None
                if self.button_lista.collidepoint(event.pos) and event.button == 1:
                    if not self.lista:
                        self.lista = Lista(self)
                    else:
                        self.lista.remove_sprite()
                        self.lista = None
                if self.player.eq_screen_active:
                    if (self.player.eq_screen.events(event)):
                        msg = pickle.dumps(self.player.eq_screen.events(event))
                        self.s.send(bytes(f"{len(msg):<{self.header}}", 'utf-8') + msg)
                        self.player_update()


    def player_update(self):
        data = b''
        new_msg = True
        while True:
            msg = self.s.recv(2048)
            if new_msg:
                msglen = int(msg[:self.header])
                new_msg = False
            data += msg
            if len(data) - self.header == msglen:
                break
        update = pickle.loads(data[self.header:])
        for obiekt in update:
            if isinstance(obiekt,sd.Player):
                for postac in self.players:
                    if postac.name == obiekt.name:
                        postac.update_client(obiekt)
                if not any(postac.name == obiekt.name for postac in self.players):
                    self.players.append(Player(self, obiekt))
            if isinstance(obiekt,sd.Skarb):
                for skarb in self.skarby:
                    if skarb.id == obiekt.id:
                        skarb.update_skarb(obiekt)
            if isinstance(obiekt,sd.Potwor):
                for potwor in self.potwory:
                    if potwor.id == obiekt.id:
                        potwor.update_client(obiekt)
            if obiekt == "przejscie":
                print("close")
                self.s.close()
                if self.port == port:
                    self.port = port1
                    self.all_sprites.empty()
                    self.create_ground()
                    self.create_socket(server, port1)
                    self.load_map()
                elif self.port == port1:
                    self.port = port
                    self.all_sprites.empty()
                    self.create_ground()
                    self.create_socket(server, port)
                    self.load_map()
            if self.player.hp <= 0 and not self.deathscreen:
                self.deathscreen = DeathScreen(self)

    def create_socket(self, server, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.s.connect((self.server, self.port))
        identifier = pickle.dumps(self.name)
        self.s.sendall(bytes(f"{len(identifier):<{self.header}}", 'utf-8') + identifier)

    def load_map(self):
        data = b''
        new_msg = True
        while True:
            msg = self.s.recv(2048)
            if new_msg:
                msglen = int(msg[:self.header])
                new_msg = False
            data += msg
            if len(data) - self.header == msglen:
                break
        data_arr = pickle.loads(data[self.header:])
        self.players = []
        self.potwory = []
        self.skarby = []
        for obiekt in data_arr:
            if isinstance(obiekt, sd.Wall):
                WallSprite(self, obiekt)
            if isinstance(obiekt, sd.Player):
                if not any(postac.name == obiekt.name for postac in self.players):
                    self.players.append(Player(self, obiekt))
                for player in self.players:
                    if player.name == self.name:
                        self.player = player
                        self.player.change_sprite(pg.image.load("Sprites/pc_main.png").convert_alpha())
                        State(self, self.player)
            if isinstance(obiekt, sd.Potwor):
                self.potwory.append(PotworSprite(self, obiekt))
            if isinstance(obiekt, sd.Skarb):
                self.skarby.append(SkarbSprite(self, obiekt))
            if isinstance(obiekt, sd.Przejscie):
                Przejscie(self, obiekt)

    def quit(self):
        self.s.close()
        pg.quit()
        sys.exit()

    def add_name(self):
        print("Podaj nazwę gracza.")
        self.name = input()

    def create_ground(self):
        self.ground = []
        self.ground.append(pg.image.load("Sprites/tile1.png"))
        self.ground.append(pg.image.load("Sprites/tile2.png"))
        for x in range(31):
            for y in range(24):
                GroundSprite(self,x,y,self.ground)


g = Gra()
while True:
    g.run()