import pygame as pg
import random
from config import *


class WallSprite(pg.sprite.Sprite):
    def __init__(self, gra, wall):
        self.groups = gra.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.gra = gra
        self.image = pg.image.load("Sprites/wall.png")
        self.rect = self.image.get_rect()
        self.x = wall.x
        self.y = wall.y
        self.rect.x = wall.x * tile
        self.rect.y = wall.y * tile

class Przejscie(pg.sprite.Sprite):
    def __init__(self, gra, przejscie):
        self.groups = gra.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.gra = gra
        self.image = pg.image.load("Sprites/przejscie.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.x = przejscie.x
        self.y = przejscie.y
        self.rect.x = self.x * tile
        self.rect.y = self.y * tile


class GroundSprite(pg.sprite.Sprite):
    def __init__(self, gra, x, y, sprites):
        self.groups = gra.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.gra = gra
        self.image = random.choice(sprites)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * tile
        self.rect.y = self.y * tile


class PotworSprite(pg.sprite.Sprite):
    def __init__(self, gra, potwor):
        self.groups = gra.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.gra = gra
        self.image = pg.image.load("Sprites/potwor.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.x = potwor.x
        self.y = potwor.y
        self.id = potwor.id
        self.hp_max = potwor.hp_max
        self.hp = self.hp_max
        self.atak = potwor.atak
        self.red = potwor.red
        self.rect.x = potwor.x * tile
        self.rect.y = potwor.y * tile
        self.aktywny = potwor.aktywny
        if not self.aktywny:
            self.remove(self.groups)

    def update_client(self, potwor):
        self.id = potwor.id
        self.hp_max = potwor.hp_max
        self.hp = potwor.hp
        self.atak = potwor.atak
        self.red = potwor.red
        self.aktywny = potwor.aktywny
        if not self.aktywny:
            self.remove(self.groups)

class SkarbSprite(pg.sprite.Sprite):
    def __init__(self, gra, skarb):
        self.groups = gra.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.gra = gra
        self.id = skarb.id
        self.image = pg.image.load("Sprites/chest.png")
        self.rect = self.image.get_rect()
        self.x = skarb.x
        self.y = skarb.y
        self.rect.x = skarb.x * tile
        self.rect.y = skarb.y * tile
        self.aktywny = skarb.aktywny
        if not self.aktywny:
            self.remove(self.groups)

    def update_skarb(self, skarb):
        self.aktywny = skarb.aktywny
        if not self.aktywny:
            self.remove(self.groups)

class Uzbrojenie:
    def __init__(self):
        self.typ = random.choice(["Broń", "Tarcza", "Pancerz", "Hełm"])
        if self.typ == "Broń":
            self.wartosc = random.randint(1, 10)
        if self.typ == "Tarcza":
            self.wartosc = random.randint(1, 15)
        if self.typ == "Pancerz" or self.typ == "Hełm":
            self.wartosc = random.randint(5, 50)
        self.id = 1

class Ekwipunek(pg.sprite.Sprite):
    def __init__(self, gra, player):
        self.groups = gra.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.gra = gra
        self.player = player
        self.player.eq_screen_active = True
        self.image = pg.Surface((szer, wys))
        self.image.fill((255, 255, 255))
        self.rect = (0, 0, szer, wys)
        self.lista_typ = []
        self.lista_wartosc = []
        self.buttons = []
        self.headerfont = pg.font.SysFont(None, 50)
        self.myfont = pg.font.SysFont(None, 40)
        for x in self.player.ekwipunek:
            if x == self.player.bron or x == self.player.helm or x == self.player.pancerz or self.player.tarcza:
                self.lista_typ.append(self.myfont.render(str(x.typ), True, color_black, (200, 200, 200)))
            else:
                self.lista_typ.append(self.myfont.render(str(x.typ), True, color_black))
            self.lista_wartosc.append(self.myfont.render(str(x.wartosc), True, color_black))
            self.buttons.append(Eq_button(x))
        self.uzbr_typ = self.headerfont.render("Typ uzbrojenia", True, color_black)
        self.uzbr_wartosc = self.headerfont.render("Bonus", True, color_black)
        self.image.blit(self.uzbr_typ, (10, 10))
        self.image.blit(self.uzbr_wartosc, (300, 10))
        self.odstep_y = 50
        for x in self.buttons:
            x.zmien_y(self.odstep_y)
            pg.draw.rect(self.image, color_white, x)
            self.odstep_y += 40
        self.odstep_y = 40
        for x in self.lista_typ:
            self.image.blit(x, (10, 10 + self.odstep_y))
            self.odstep_y += 40
        self.odstep_y = 40
        for x in self.lista_wartosc:
            self.image.blit(x, (300, 10 + self.odstep_y))
            self.odstep_y += 40

    def update(self):
        self.lista_typ = []
        self.lista_wartosc = []
        self.buttons = []
        self.image.fill((255, 255, 255))
        for x in self.player.ekwipunek:
            if x == self.player.bron:
                self.lista_typ.append(self.myfont.render(str(x.typ), True, color_black, (200, 200, 200)))
            elif x == self.player.helm:
                self.lista_typ.append(self.myfont.render(str(x.typ), True, color_black, (200, 200, 200)))
            elif x == self.player.pancerz:
                self.lista_typ.append(self.myfont.render(str(x.typ), True, color_black, (200, 200, 200)))
            elif x == self.player.tarcza:
                self.lista_typ.append(self.myfont.render(str(x.typ), True, color_black, (200, 200, 200)))
            else:
                self.lista_typ.append(self.myfont.render(str(x.typ), True, color_black))
            self.lista_wartosc.append(self.myfont.render(str(x.wartosc), True, color_black))
            self.buttons.append(Eq_button(x))
        self.uzbr_typ = self.headerfont.render("Typ uzbrojenia", True, color_black)
        self.uzbr_wartosc = self.headerfont.render("Bonus", True, color_black)
        self.image.blit(self.uzbr_typ, (10, 10))
        self.image.blit(self.uzbr_wartosc, (300, 10))
        self.odstep_y = 50
        for x in self.buttons:
            x.zmien_y(self.odstep_y)
            pg.draw.rect(self.image, (255, 255, 255), x.rect)
            self.odstep_y += 40
        self.odstep_y = 40
        for x in self.lista_typ:
            self.image.blit(x, (10, 10 + self.odstep_y))
            self.odstep_y += 40
        self.odstep_y = 40
        for x in self.lista_wartosc:
            self.image.blit(x, (300, 10 + self.odstep_y))
            self.odstep_y += 40

    def zamknij(self):
        self.player.eq_screen_active = False
        self.remove(self.groups)

    def events(self, event):
        for x in self.buttons:
            if x.rect.collidepoint(event.pos):
                return x.uzbrojenie


class Eq_button:
    def __init__(self, uzbrojenie, y=10):
        self.uzbrojenie = uzbrojenie
        self.rect = pg.Rect(10, y, 400, 26)

    def zmien_y(self, y):
        self.rect = pg.Rect(10, y, 400, 26)


class Player(pg.sprite.Sprite):
    def __init__(self, gra, player):
        self.groups = gra.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.gra = gra
        self.image = pg.image.load("Sprites/pc.png").convert_alpha()
        #self.image.fill(color_player)
        self.rect = self.image.get_rect()
        self.x = player.x
        self.y = player.y
        self.id = player.id
        self.name = player.name
        self.poziom = player.poziom
        self.hp_max = player.hp_max
        self.hp = player.hp
        self.atak = player.atak
        self.red = player.red
        self.exp = player.exp
        self.exp_next = player.exp_next
        self.mp_max = player.mp_max
        self.mp = player.mp
        self.walka = player.walka
        self.potyczka = None
        self.przeciwnik = player.przeciwnik
        self.eq_screen_active = player.eq_screen_active
        self.ekwipunek = player.ekwipunek
        self.bron = player.bron
        self.helm = player.helm
        self.tarcza = player.tarcza
        self.pancerz = player.pancerz
        self.aktywny = player.aktywny
        if not self.aktywny:
            self.remove(self.groups)


    def update_client(self, player):
        self.x = player.x
        self.y = player.y
        self.poziom = player.poziom
        self.hp_max = player.hp_max
        self.hp = player.hp
        self.atak = player.atak
        self.red = player.red
        self.exp = player.exp
        self.exp_next = player.exp_next
        self.mp_max = player.mp_max
        self.mp = player.mp
        self.przeciwnik = player.przeciwnik
        self.walka = player.walka
        self.ekwipunek = player.ekwipunek
        self.bron = player.bron
        self.helm = player.helm
        self.tarcza = player.tarcza
        self.pancerz = player.pancerz
        self.aktywny = player.aktywny
        if self.walka and not self.potyczka:
            for potwor in self.gra.potwory:
                if self.przeciwnik.id == potwor.id:
                    self.potyczka = Walka(self.gra, self, potwor)
        if not self.walka and self.potyczka:
            self.potyczka.remove_sprite()
            self.potyczka = None
        if not self.aktywny:
            self.remove(self.groups)

    def update(self):
        self.rect.x = self.x * tile
        self.rect.y = self.y * tile

    def otworz_eq(self):
        if not self.eq_screen_active:
            self.eq_screen = Ekwipunek(self.gra, self)
        else:
            self.eq_screen.zamknij()

    def change_sprite(self, sprite):
        self.image = sprite


class State(pg.sprite.Sprite):
    def __init__(self, gra, player):
        self.groups = gra.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.gra = gra
        self.player = player
        self.image = pg.Surface((szer - 512, 512))
        self.image.fill(color_white)
        self.rect = (512, 0, szer - 512, 128)
        self.myfont = pg.font.SysFont(None, 40)
        self.stat1 = self.myfont.render("Poziom " + str(self.player.poziom), True, color_black)
        self.stat_exp = self.myfont.render("Exp " + str(self.player.exp) + "/" + str(self.player.exp_next), True,
                                           color_black)
        self.stat2 = self.myfont.render("HP: " + str(self.player.hp) + "/" + str(self.player.hp_max), True, color_black)
        self.stat_mp = self.myfont.render("MP: " + str(self.player.mp) + "/" + str(self.player.mp_max), True,
                                          color_black)
        self.stat_atak = self.myfont.render("Atak: " + str(self.player.atak), True, color_black)
        self.stat_red = self.myfont.render("Redukcja: " + str(self.player.red), True, color_black)
        self.uzbrojenie = self.myfont.render("Uzbrojenie", True, color_black)
        if self.player.bron:
            self.bron = self.myfont.render("Broń" + " (" + str(self.player.bron.wartosc) + ")", True, color_black)
        else:
            self.bron = self.myfont.render("Broń" + " (Brak)", True, color_black)
        if self.player.helm:
            self.helm = self.myfont.render("Hełm" + " (" + str(self.player.helm.wartosc) + ")", True, color_black)
        else:
            self.helm = self.myfont.render("Hełm" + " (Brak)", True, color_black)
        if self.player.pancerz:
            self.pancerz = self.myfont.render("Hełm" + " (" + str(self.player.pancerz.wartosc) + ")", True, color_black)
        else:
            self.pancerz = self.myfont.render("Hełm" + " (Brak)", True, color_black)
        if self.player.tarcza:
            self.tarcza = self.myfont.render("Hełm" + " (" + str(self.player.tarcza.wartosc) + ")", True, color_black)
        else:
            self.tarcza = self.myfont.render("Hełm" + " (Brak)", True, color_black)
        self.image.blit(self.stat1, (10, 10))
        self.image.blit(self.stat_exp, (10, 40))
        self.image.blit(self.stat2, (10, 70))
        self.image.blit(self.stat_mp, (10, 100))
        self.image.blit(self.stat_atak, (10, 130))
        self.image.blit(self.stat_red, (10, 160))
        self.image.blit(self.uzbrojenie, (10, 200))
        if self.bron:
            self.image.blit(self.bron, (10, 230))
        if self.tarcza:
            self.image.blit(self.tarcza, (10, 250))
        if self.helm:
            self.image.blit(self.helm, (10, 280))
        if self.pancerz:
            self.image.blit(self.pancerz, (10, 310))

    def update(self):
        self.image.fill(color_white)
        self.stat1 = self.myfont.render("Poziom " + str(self.player.poziom), True, color_black)
        self.stat_exp = self.myfont.render("Exp " + str(self.player.exp) + "/" + str(self.player.exp_next), True,
                                           color_black)
        self.stat2 = self.myfont.render("HP: " + str(self.player.hp) + "/" + str(self.player.hp_max), True, color_black)
        self.stat_mp = self.myfont.render("MP: " + str(self.player.mp) + "/" + str(self.player.mp_max), True,
                                          color_black)
        self.stat_atak = self.myfont.render("Atak: " + str(self.player.atak), True, color_black)
        self.stat_red = self.myfont.render("Redukcja: " + str(self.player.red), True, color_black)
        if self.player.bron:
            self.bron = self.myfont.render("Broń" + " (" + str(self.player.bron.wartosc) + ")", True, color_black)
        else:
            self.bron = self.myfont.render("Broń" + " (Brak)", True, color_black)
        if self.player.helm:
            self.helm = self.myfont.render("Hełm" + " (" + str(self.player.helm.wartosc) + ")", True, color_black)
        else:
            self.helm = self.myfont.render("Hełm" + " (Brak)", True, color_black)
        if self.player.pancerz:
            self.pancerz = self.myfont.render("Pancerz" + " (" + str(self.player.pancerz.wartosc) + ")", True,
                                              color_black)
        else:
            self.pancerz = self.myfont.render("Pancerz" + " (Brak)", True, color_black)
        if self.player.tarcza:
            self.tarcza = self.myfont.render("Tarcza" + " (" + str(self.player.tarcza.wartosc) + ")", True, color_black)
        else:
            self.tarcza = self.myfont.render("Tarcza" + " (Brak)", True, color_black)
        self.image.blit(self.stat1, (10, 10))
        self.image.blit(self.stat_exp, (10, 50))
        self.image.blit(self.stat2, (10, 90))
        self.image.blit(self.stat_mp, (10, 130))
        self.image.blit(self.stat_atak, (10, 170))
        self.image.blit(self.stat_red, (10, 210))
        self.image.blit(self.uzbrojenie, (10, 250))
        self.image.blit(self.bron, (10, 290))
        self.image.blit(self.tarcza, (10, 330))
        self.image.blit(self.helm, (10, 370))
        self.image.blit(self.pancerz, (10, 410))


class Walka(pg.sprite.Sprite):
    def __init__(self, gra, player, przeciwnik):
        self.groups = gra.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.gra = gra
        self.player = player
        self.przeciwnik = przeciwnik
        self.image = pg.Surface((szer, wys))
        self.image.fill(color_white)
        self.rect = (0, 0, szer, wys)
        self.myfont = pg.font.SysFont(None, 45)
        self.player_hp = self.myfont.render("Zdrowie: " + str(self.player.hp), True, color_black)
        self.player_atak = self.myfont.render("Atak: " + str(self.player.atak), True, color_black)
        self.player_red = self.myfont.render("Redukcja: " + str(self.player.red), True, color_black)
        self.player_mp = self.myfont.render("MP: " + str(self.player.mp) + "/" + str(self.player.mp_max), True,
                                            color_black)
        self.przeciwnik_hp = self.myfont.render("Zdrowie: " + str(self.przeciwnik.hp), True, color_black)
        self.przeciwnik_atak = self.myfont.render("Atak: " + str(self.przeciwnik.atak), True, color_black)
        self.przeciwnik_redukcja = self.myfont.render("Redukcja: " + str(self.przeciwnik.red), True, color_black)
        self.gracz = self.myfont.render("Ty", True, color_black)
        self.wrog = self.myfont.render("Wróg", True, color_black)
        self.atak = self.myfont.render("1) Zwykły atak", True, color_black)
        self.heal = self.myfont.render("2) Uzdrowienie (15 MP)", True, color_black)
        self.regen = self.myfont.render("3) Regeneracja mp", True, color_black)
        self.precatak = self.myfont.render("4) Atak precyzyjny (ignoruje pancerz, 10 MP)", True, color_black)
        self.potatak = self.myfont.render("5) Potężny atak (atak * 1.5, 10 MP)", True, color_black)
        self.image.blit(self.gracz, (10, 10))
        self.image.blit(self.wrog, (350, 10))
        self.image.blit(self.player_hp, (10, 40))
        self.image.blit(self.przeciwnik_hp, (350, 40))
        self.image.blit(self.player_atak, (10, 70))
        self.image.blit(self.przeciwnik_atak, (350, 70))
        self.image.blit(self.player_red, (10, 100))
        self.image.blit(self.przeciwnik_redukcja, (350, 100))
        self.image.blit(self.player_mp, (10, 130))
        self.image.blit(self.atak, (10, 190))
        self.image.blit(self.heal, (10,220))
        self.image.blit(self.regen, (10,250))
        self.image.blit(self.precatak, (10,280))
        self.image.blit(self.potatak, (10,310))

    def update(self):
        self.image.fill(color_white)
        self.player_hp = self.myfont.render("Zdrowie: " + str(self.player.hp), True, color_black)
        self.player_atak = self.myfont.render("Atak: " + str(self.player.atak), True, color_black)
        self.player_red = self.myfont.render("Redukcja: " + str(self.player.red), True, color_black)
        self.player_mp = self.myfont.render("MP: " + str(self.player.mp) + "/" + str(self.player.mp_max), True,
                                            color_black)
        self.przeciwnik_hp = self.myfont.render("Zdrowie: " + str(self.przeciwnik.hp), True, color_black)
        self.przeciwnik_atak = self.myfont.render("Atak: " + str(self.przeciwnik.atak), True, color_black)
        self.przeciwnik_redukcja = self.myfont.render("Redukcja: " + str(self.przeciwnik.red), True, color_black)
        self.image.blit(self.gracz, (10, 10))
        self.image.blit(self.wrog, (350, 10))
        self.image.blit(self.player_hp, (10, 40))
        self.image.blit(self.przeciwnik_hp, (350, 40))
        self.image.blit(self.player_atak, (10, 70))
        self.image.blit(self.przeciwnik_atak, (350, 70))
        self.image.blit(self.player_red, (10, 100))
        self.image.blit(self.przeciwnik_redukcja, (350, 100))
        self.image.blit(self.player_mp, (10, 130))
        self.image.blit(self.atak, (10, 190))
        self.image.blit(self.heal, (10, 220))
        self.image.blit(self.regen, (10, 250))
        self.image.blit(self.precatak, (10, 280))
        self.image.blit(self.potatak, (10, 310))

    def remove_sprite(self):
        self.remove(self.groups)

class Instrukcja(pg.sprite.Sprite):
    def __init__(self, gra):
        self.groups = gra.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((szer, wys))
        self.image.fill((255, 255, 255))
        self.rect = (0, 0, szer, wys)
        self.myfont = pg.font.SysFont(None, 35)
        self.headerfont = pg.font.SysFont(None, 50)
        self.header1 = self.headerfont.render("Sterowanie", True, color_black)
        self.up = self.myfont.render("Ruch w górę: klawisz w lub strzałka w górę.", True, color_black)
        self.down = self.myfont.render("Ruch w dół: klawisz s lub strzałka w dół.", True, color_black)
        self.right = self.myfont.render("Ruch w prawo: klawisz d lub strzałka w prawo.", True, color_black)
        self.left = self.myfont.render("Ruch w lewo: klawisz a lub strzałka w lewo", True, color_black)
        self.walka = self.myfont.render("W walce akcje wykonywane są za pomocą klawiszy 1-5", True, color_black)
        self.header2 = self.headerfont.render("Skróty klawiszowe", True, color_black)
        self.ekwipunek = self.myfont.render("I: Okno ekwipunku", True, color_black)
        self.instrukcja = self.myfont.render("H: Instrukcja", True, color_black)
        self.lista = self.myfont.render("O: Lista graczy", True, color_black)
        self.image.blit(self.header1, (10, 10))
        self.image.blit(self.up, (10, 50))
        self.image.blit(self.down, (10, 80))
        self.image.blit(self.right, (10, 110))
        self.image.blit(self.left, (10, 140))
        self.image.blit(self.walka, (10, 170))
        self.image.blit(self.header2, (10, 210))
        self.image.blit(self.ekwipunek, (10, 250))
        self.image.blit(self.instrukcja, (10, 280))
        self.image.blit(self.lista, (10, 310))

    def update(self):
        self.image.fill((255, 255, 255))
        self.image.blit(self.header1, (10, 10))
        self.image.blit(self.up, (10, 50))
        self.image.blit(self.down, (10, 80))
        self.image.blit(self.right, (10, 110))
        self.image.blit(self.left, (10, 140))
        self.image.blit(self.walka, (10, 170))
        self.image.blit(self.header2, (10, 210))
        self.image.blit(self.ekwipunek, (10, 250))
        self.image.blit(self.instrukcja, (10, 280))
        self.image.blit(self.lista, (10, 310))
		
		
    def remove_sprite(self):
        self.remove(self.groups)

class Lista(pg.sprite.Sprite):
    def __init__(self, gra):
        self.gra = gra
        self.groups = gra.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((szer, wys))
        self.image.fill((255, 255, 255))
        self.rect = (0, 0, szer, wys)
        self.myfont = pg.font.SysFont(None, 40)
        self.headerfont = pg.font.SysFont(None, 50)
        self.players = []
        self.players_poziom = []
        self.header1 = self.headerfont.render("Lista graczy", True, color_black)
        self.nazwa = self.myfont.render("Nazwa" + "               " + "Poziom", True, color_black)
        for player in self.gra.players:
            self.players.append(self.myfont.render(str(player.name), True, color_black))
            self.players_poziom.append(self.myfont.render(str(player.poziom),True, color_black))
        y = 90
        self.image.blit(self.header1, (10,10))
        self.image.blit(self.nazwa, (10, 50))
        for player in self.players:
            self.image.blit(player, (10,y))
            y += 40
        y = 90
        for poziom in self.players_poziom:
            self.image.blit(poziom, (225, y))
            y += 40

    def update(self):
        self.image.fill((255, 255, 255))
        self.players = []
        self.players_poziom = []
        for player in self.gra.players:
            self.players.append(self.myfont.render(str(player.name), True, color_black))
            self.players_poziom.append(self.myfont.render(str(player.poziom),True, color_black))
        self.image.blit(self.header1, (10, 10))
        self.image.blit(self.nazwa, (10, 50))
        y = 90
        for player in self.players:
            self.image.blit(player, (10, y))
            y += 40
        y = 90
        for poziom in self.players_poziom:
            self.image.blit(poziom, (225, y))
            y += 40


    def remove_sprite(self):
        self.remove(self.groups)

class DeathScreen(pg.sprite.Sprite):
    def __init__(self, gra):
        self.gra = gra
        self.groups = gra.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.Surface((szer, wys))
        self.image.fill((255, 255, 255))
        self.rect = (0, 0, szer, wys)
        self.myfont = pg.font.SysFont(None, 60)
        self.inf = self.myfont.render("Twoja postać zginęła.", True, color_black)
        self.image.blit(self.inf, (szer/2-200,wys/2-60))

    def update(self):
        self.image.fill(color_white)
        self.image.blit(self.inf, (szer/2-200,wys/2-60))

