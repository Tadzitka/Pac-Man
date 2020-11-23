import pgzrun
import random

WIDTH = 1920
HEIGHT = 1024
TITLE = "Pan pizza"
plansza = []


class Pacman(Actor):
    def __init__(self, x, y, kos):
        super(Pacman, self).__init__(kos, (x, y))
        self.pos = x, y
        self.czy_lustro = False
        self.fps = 0
        self.kat = 0
        self.blok = False

    def draw(self):
        super(Pacman, self).draw()

    def update(self):
        self.fps += 1
        self.fps = self.fps % 30
        if self.fps < 15:
            if self.czy_lustro == True:
                self.image = "pac_3"
            else:
                self.image = "pac_2"
        else:
            if self.czy_lustro == True:
                self.image = "pac_4"
            else:
                self.image = "pac_1"
        self.angle = self.kat
        d = self.pos[0] // 32
        e = self.pos[1] // 32
        # print(d,e,self.pos)
        if d * 32 == self.pos[0] and e * 32 == self.pos[1]:
            self.blok = False

    def up(self):
        if self.blok == False:
            self.czy_lustro = False
            self.kat = 90
            self.blok = True
            animate(self, tween='linear', duration=0.7, pos=(self.pos[0], self.pos[1] - 64))

    def down(self):
        if self.blok == False:
            self.czy_lustro = False
            self.kat = -90
            self.blok = True
            animate(self, tween='linear', duration=0.7, pos=(self.pos[0], self.pos[1] + 64))

    def left(self):
        if self.blok == False:
            self.czy_lustro = True
            self.kat = 0
            x = self.pos
            self.blok = True
            animate(self, tween='linear', duration=0.7, pos=(self.pos[0] - 64, self.pos[1]))

    def right(self):
        if self.blok == False:
            self.czy_lustro = False
            self.kat = 0
            x = self.pos
            self.blok = True
            animate(self, tween='linear', duration=0.7, pos=(self.pos[0] + 64, self.pos[1]))


class Duszek(Actor):
    def __init__(self, x, y, kos, numer):
        super(Duszek, self).__init__(kos, (x, y))
        self.pos = x, y
        self.czy_lustro = False
        self.fps = 0
        self.kat = 0
        self.blok = False
        self.numer = numer

    def update(self):
        self.fps += 1
        self.fps = self.fps % 30
        if self.fps < 15:
            if self.czy_lustro == True:
                self.image = f"duch{self.numer}a"
            else:
                self.image = f"duch{self.numer}al"
        else:
            if self.czy_lustro == True:
                self.image = f"duch{self.numer}b"
            else:
                self.image = f"duch{self.numer}bl"
        self.angle = self.kat
        d = self.pos[0] // 32
        e = self.pos[1] // 32
        # self.blok = False
        print(d, e, self.pos)
        if d * 32 == self.pos[0] and e * 32 == self.pos[1]:
            self.blok = False

    def up(self):
        if self.blok == False:
            self.czy_lustro = False
            self.blok = True
            animate(self, tween='linear', duration=0.7, pos=(self.pos[0], self.pos[1]-64))

    def down(self):
        if self.blok == False:
            self.czy_lustro = False
            self.blok = True
            animate(self, tween='linear', duration=0.7, pos=(self.pos[0], self.pos[1] + 64))
    def left(self):
        if self.blok == False:
            self.czy_lustro = True
            x = self.pos
            self.blok = True
            animate(self, tween='linear', duration=0.7, pos=(self.pos[0] - 64, self.pos[1]))

    def right(self):
        if self.blok == False:
            self.czy_lustro = False
            x = self.pos
            self.blok = True
            animate(self, tween='linear', duration=0.7, pos=(self.pos[0] + 64, self.pos[1]))


class Mapa():
    def __init__(self):
        self.gracz = Pacman(1824, 928, "pac_1")
        self.plansza = []
        self.licznik = 0
        f = open("plansza").read()
        f = f.split()
        for i in f:
            self.plansza.append(list(i))
        self.duszki = [Duszek(928, 480, "duch1a", 1), Duszek(1056, 480, "duch2a", 2), Duszek(1184, 480, "duch3a", 3), Duszek(1312, 480, "duch4a", 4)]
        self.ilosc_rochow = 0

    def kolizja(self, x, y):
        """zwraca krotkę (up,down,left,right)"""
        x = int(x // 64)
        y = int(y // 64)
        if y - 1 >= 0 and (self.plansza[y - 1][x] == "0" or self.plansza[y - 1][x] == "9" or self.plansza[y - 1][x] == "3"):
            up = True
        else:
            up = False
        if y + 1 <= (len(self.plansza)) and (self.plansza[y + 1][x] == "0" or self.plansza[y + 1][x] == "9" or self.plansza[y + 1][x] == "3"):
            down = True
        else:
            down = False
        if x - 1 >= 0 and (self.plansza[y][x - 1] == "0" or self.plansza[y][x - 1] == "9" or self.plansza[y][x - 1] == "3"):
            left = True
        else:
            left = False
        if x + 1 <= (len(self.plansza[y])) and (self.plansza[y][x + 1] == "0" or self.plansza[y][x + 1] == "9" or self.plansza[y][x + 1] == "3"):
            right = True
        else:
            right = False
        return (up, down, left, right)

    def jedzenie(self, x, y):
        x = int(x // 64)
        y = int(y // 64)
        # print(x, y)
        if self.plansza[y][x] == "0":
            self.licznik += 10
            self.plansza[y][x] = "9"
    def ai_duchow(self):
        for i in range (4):
            # 0 - up, 1 - down, 2 - left, 3 - right
            ruch = self.kolizja(self.duszki[i].pos[0], self.duszki[i].pos[1])
            losowa = random.randint(0, 3)
            while(ruch[losowa] != True):
                losowa = random.randint(0, 3)
            if losowa == 0:
                self.duszki[i].up()
            elif losowa == 1:
                self.duszki[i].down()
            elif losowa == 2:
                self.duszki[i].left()
            elif losowa == 3:
                self.duszki[i].right()
            print(ruch)
    def draw(self):
        screen.clear()
        for i in range(len(mapa.plansza)):
            for j in range(len(mapa.plansza[i])):
                if mapa.plansza[i][j] == "1":
                    screen.blit("sciana", (j * 64, i * 64))
                if mapa.plansza[i][j] == "0":
                    screen.blit("moneta", ((j * 64) + 22, (i * 64) + 22))
                if mapa.plansza[i][j] == "3":
                    screen.blit("drzwi", (j * 64, i * 64))
                if mapa.plansza[i][j] == "5":
                    screen.blit("pac_2", (j * 64, i * 64))
        for i in range (4):
            self.duszki[i].draw()
        self.gracz.draw()
        screen.draw.text(str(self.licznik), (30, 20), color="red", fontsize=60)

    def update(self):
        self.gracz.update()
        for i in range(4):
            self.duszki[i].update()
        self.ai_duchow()
        self.jedzenie(self.gracz.pos[0], self.gracz.pos[1])
        ruchy = self.kolizja(self.gracz.pos[0], self.gracz.pos[1])
        if keyboard.up and ruchy[0] == True:
            self.gracz.up()
            #self.duszki.up()
        if keyboard.down and ruchy[1] == True:
            self.gracz.down()
            #self.duszki.down()
        if keyboard.right and ruchy[3] == True:
            self.gracz.right()
            #self.duszki.right()
        if keyboard.left and ruchy[2] == True:
            self.gracz.left()
            #self.duszki.left()
        # print("licznik:", self.licznik)


fps = 0

mapa = Mapa()


def draw():
    mapa.draw()


def update():
    mapa.update()


pgzrun.go()
