import pgzrun

WIDTH = 1920
HEIGHT = 1024
plansza = []

class Pacman(Actor):
    def __init__(self,x,y,kos):
        super(Pacman, self).__init__(kos, (x, y))
        self.pos = x,y
        self.czy_lustro = False
        self.fps = 0
        self.kat = 0
        self.blok =False
    def draw(self):
        super(Pacman,self).draw()
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
        d = self.pos [0]//32
        e = self.pos [1]//32
        print(d,e,self.pos)
        if d * 32 == self.pos [0] and e * 32 == self.pos [1]:
            self.blok = False
    def up(self):
        if self.blok == False:
            self.czy_lustro = False
            self.kat = 90
            self.blok = True
            animate(self,tween='linear',duration=0.7, pos=(self.pos[0], self.pos[1]-64))
    def down(self):
        if self.blok == False:
            self.czy_lustro = False
            self.kat = -90
            self.blok = True
            animate(self,tween='linear',duration=0.7, pos=(self.pos[0], self.pos[1] + 64))
    def left(self):
        if self.blok == False:
            self.czy_lustro = True
            self.kat = 0
            x = self.pos
            self.blok = True
            animate(self,tween='linear',duration=0.7, pos=(self.pos[0] - 64, self.pos[1]))
    def right(self):
        if self.blok == False:
            self.czy_lustro = False
            self.kat = 0
            x = self.pos
            self.blok = True
            animate(self,tween='linear',duration=0.7, pos=(self.pos[0] + 64, self.pos[1]))
class Mapa():
    def __init__(self):
        self.gracz = Pacman(1824, 928, "pac_1")
        self.plansza = []
        self.licznik = 0
        f = open("plansza").read()
        f = f.split()
        for i in f:
            self.plansza.append(list(i))
    def kolizja(self, x, y):
        """zwraca krotkę (up,down,left,right)"""
        x=int(x//64)
        y=int(y//64)
        if y - 1 >= 0 and (self.plansza [y-1][x] == "0" or self.plansza [y-1][x] == "9"):
            up = True
        else:
            up = False
        if y + 1 <= (len(self.plansza)) and (self.plansza[y + 1][x] == "0" or self.plansza[y + 1][x] == "9"):
            down = True
        else:
            down = False
        if x - 1 >= 0 and (self.plansza [y][x-1] == "0" or self.plansza [y][x-1] == "9"):
            left = True
        else:
            left = False
        if x + 1 <= (len(self.plansza[y])) and (self.plansza[y][x+1] == "0" or self.plansza[y][x+1] == "9"):
            right = True
        else:
            right = False
        return(up,down,left,right)
    def jedzenie(self, x, y):
        x = int(x // 64)
        y = int(y // 64)
        print(x, y)
        if self.plansza[y][x] == "0":
            self.licznik += 10
            self.plansza[y][x] = "9"
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
        self.gracz.draw()
        screen.draw.text(str(self.licznik), (30, 20), color="red", fontsize=60)
    def update(self):
        self.gracz.update()
        self.jedzenie(self.gracz.pos[0],self.gracz.pos[1])
        ruchy = self.kolizja(self.gracz.pos[0],self.gracz.pos[1])
        if keyboard.up and ruchy[0] == True:
            self.gracz.up()
        if keyboard.down and ruchy[1] == True:
            self.gracz.down()
        if keyboard.right and ruchy[3] == True:
            self.gracz.right()
        if keyboard.left and ruchy[2] == True:
            self.gracz.left()
        print("licznik:", self.licznik)

fps = 0


mapa = Mapa()

def draw():
    mapa.draw()
def update():
    mapa.update()




pgzrun.go()