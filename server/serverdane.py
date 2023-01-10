import random
import threading as thread

class Wall:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Przejscie:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Uzbrojenie:
    def __init__(self, id):
        self.typ = random.choice(["Broń", "Tarcza", "Pancerz", "Hełm"])
        if self.typ == "Broń":
            self.wartosc = random.randint(1, 10)
        if self.typ == "Tarcza":
            self.wartosc = random.randint(1, 15)
        if self.typ == "Pancerz" or self.typ == "Hełm":
            self.wartosc = random.randint(5, 50)
        self.id = id


class Potwor:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.hp_max = 100
        self.hp = self.hp_max
        self.atak = 10
        self.red = 5
        self.aktywny = True
        self.zajety = False

class Skarb:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.skarb = Uzbrojenie(id)
        self.aktywny = True

    def podnies(self):
        self.skarb = None
        self.aktywny = False


class Player:
    def __init__(self, x, y, id, name):
        self.x = x
        self.y = y
        self.id = id
        self.name = name
        self.poziom = 1
        self.hp_max = 100
        self.hp = self.hp_max
        self.atak = 20
        self.red = 0
        self.exp = 0
        self.exp_next = 100
        self.mp_max = 100
        self.mp = self.mp_max
        self.walka = False
        self.battle = None
        self.przeciwnik = None
        self.eq_screen_active = False
        self.ekwipunek = []
        self.bron = None
        self.helm = None
        self.tarcza = None
        self.pancerz = None
        self.aktywny = False

    def update(self, player):
        self.poziom = player.poziom
        self.hp_max = player.hp_max
        self.hp = player.hp
        self.atak = player.atak
        self.red = player.red
        self.exp = player.exp
        self.exp_next = player.exp_next
        self.mp_max = player.mp_max
        self.mp = player.mp
        for ekwipunek in player.ekwipunek:
            if not any(ekwipunek.id == ekw.id for ekw in self.ekwipunek):
                self.ekwipunek.append(ekwipunek)
        self.bron = player.bron
        self.helm = player.helm
        self.tarcza = player.tarcza
        self.pancerz = player.pancerz

    def collision_wall(self, walls, dx=0, dy=0):
        for wall in walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def move(self, walls, skarby, potwory, dx=0, dy=0):
        if not self.collision_wall(walls, dx, dy) and self.aktywny:
            if self.collision_mobs(potwory, dx, dy):
                print("Walka" + str(self.which_mob(potwory, dx, dy)))
                self.battle = Walka(self, self.which_mob(potwory, dx, dy))
            self.podnies(skarby,dx,dy)
            self.x += dx
            self.y += dy

    def collision_mobs(self, potwory, dx = 0, dy = 0):
        for potwor in potwory:
            if potwor.x == self.x + dx and potwor.y == self.y + dy and potwor.aktywny and not potwor.zajety:
                return True
        return False

    def przejscie(self, przejscie, dx = 0, dy = 0):
        for przejscie in przejscie:
            if przejscie.x == self.x + dx and przejscie.y == self.y + dy:
                return True
        return False

    def which_mob(self, potwory, dx=0, dy=0):
        for potwor in potwory:
            if potwor.x == self.x + dx and potwor.y == self.y + dy:
                return potwor

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def raiseexp(self, exp=65):
        self.exp += exp
        if self.exp >= self.exp_next:
            self.awans(self.exp - self.exp_next)

    def awans(self, exp):
        self.exp = exp
        self.exp_next += 100
        self.poziom += 1
        self.atak += 5
        self.hp_max += 10
        self.hp = self.hp_max
        self.mp_max += 10
        self.mp = self.mp_max

    def podnies(self, skarby, dx=0, dy=0):
        skarb_id = None
        for skarb in skarby:
            if skarb.x == self.x + dx and skarb.y == self.y + dy and skarb.aktywny:
                self.ekwipunek.append(skarb.skarb)
                skarb.podnies()

    def zaloz_eq(self, uzbrojenie):
        if uzbrojenie.typ == "Broń":
            if self.bron == None:
                self.bron = uzbrojenie
                self.atak += uzbrojenie.wartosc
            elif self.bron == uzbrojenie:
                self.bron = None
                self.atak -= uzbrojenie.wartosc
            else:
                self.atak -= self.bron.wartosc
                self.atak += uzbrojenie.wartosc
                self.bron = uzbrojenie
        elif uzbrojenie.typ == "Tarcza":
            if self.tarcza == None:
                self.tarcza = uzbrojenie
                self.red += uzbrojenie.wartosc
            elif self.tarcza == uzbrojenie:
                self.tarcza = None
                self.red -= uzbrojenie.wartosc
            else:
                self.red -= self.tarcza.wartosc
                self.red += uzbrojenie.wartosc
                self.tarcza = uzbrojenie
        elif uzbrojenie.typ == "Pancerz":
            if self.pancerz == None:
                self.pancerz = uzbrojenie
                self.hp_max += uzbrojenie.wartosc
                self.hp += uzbrojenie.wartosc
            elif self.pancerz == uzbrojenie:
                self.pancerz = None
                self.hp_max -= uzbrojenie.wartosc
                if self.hp - uzbrojenie.wartosc < 0:
                    self.hp = 1
                else:
                    self.hp -= uzbrojenie.wartosc
            else:
                self.hp_max -= self.pancerz.wartosc
                if self.hp - self.pancerz.wartosc < 0:
                    self.hp = 1
                else:
                    self.hp -= self.pancerz.wartosc
                self.hp_max += uzbrojenie.wartosc
                self.hp += uzbrojenie.wartosc
                self.pancerz = uzbrojenie
        elif uzbrojenie.typ == "Hełm":
            if self.helm == None:
                self.helm = uzbrojenie
                self.mp_max += uzbrojenie.wartosc
                self.mp += uzbrojenie.wartosc
            elif self.helm == uzbrojenie:
                self.helm = None
                self.mp_max -= uzbrojenie.wartosc
                if self.mp - uzbrojenie.wartosc < 0:
                    self.mp = 0
                else:
                    self.mp -= uzbrojenie.wartosc
            else:
                self.mp_max -= self.helm.wartosc
                if self.mp - self.helm.wartosc < 0:
                    self.mp = 0
                else:
                    self.mp -= self.helm.wartosc
                self.mp_max += uzbrojenie.wartosc
                self.mp += uzbrojenie.wartosc
                self.helm = uzbrojenie

class Walka:
    def __init__(self, player, przeciwnik):
        self.player = player
        self.przeciwnik = przeciwnik
        self.player.walka = True
        self.player.przeciwnik = self.przeciwnik
        self.przeciwnik.zajety = True

    def end_fight_z(self):
        self.player.walka = False
        self.player.raiseexp(exp=50)
        self.przeciwnik.aktywny = False
        self.player.przeciwnik = None
        self.player.battle = None

    def end_fight_p(self):
        self.player.walka = False
        self.player.przeciwnik = None
        self.player.battle = None
        self.player.aktywny = False
        self.przeciwnik.zajety = False

    def atak_zwykly(self):
        if self.player.atak > self.przeciwnik.red:
            self.przeciwnik.hp = self.przeciwnik.hp - (self.player.atak - self.przeciwnik.red)
        else:
            self.przeciwnik.hp -= 5
        if self.przeciwnik.hp <= 0:
            self.end_fight_z()
        else:
            self.kontratak()

    def heal(self):
        if self.player.mp > 15:
            if self.player.hp_max - int(self.player.hp_max * 0.15) > self.player.hp_max:
                self.player.hp = self.player.hp_max
                self.player.mp -= 15
            else:
                self.player.hp += int(self.player.hp_max * 0.15)
                self.player.mp -= 15
            self.kontratak()

    def mp_regen(self):
        if self.player.mp_max + int(self.player.mp_max * 0.15) > self.player.mp_max:
            self.player.mp = self.player.mp_max
        else:
            self.player.mp += int(self.player.mp_max * 0.15)
        self.kontratak()

    def atak_precyzyjny(self):
        if self.player.mp > 10:
            self.przeciwnik.hp -= self.player.atak
            self.player.mp -= 10
            if self.przeciwnik.hp <= 0:
                self.end_fight_z()
            else:
                self.kontratak()

    def atak_potezny(self):
        if self.player.mp > 10:
            self.przeciwnik.hp = self.przeciwnik.hp - (int(self.player.atak * 1.5) - self.przeciwnik.red)
            self.player.mp -= 10
            if self.przeciwnik.hp <= 0:
                self.end_fight_z()
            else:
                self.kontratak()

    def kontratak(self):
        if self.przeciwnik.atak > self.player.red:
            if self.player.hp - (self.przeciwnik.atak - self.player.red) > 0:
                self.player.hp = self.player.hp - (self.przeciwnik.atak - self.player.red)
            else:
                self.player.hp = 0
                self.end_fight_p()
        else:
            if self.player.hp - (self.przeciwnik.atak - self.player.red) > 0:
                self.player.hp -= 5
            else:
                self.player.hp = 0
                self.end_fight_p()