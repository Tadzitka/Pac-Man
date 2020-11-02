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
    def up(self):
        self.czy_lustro = False
        self.kat = 90
        self.y -= 2
    def down(self):
        self.czy_lustro = False
        self.kat = -90
        self.y += 2
    def left(self):
        self.czy_lustro = True
        self.kat = 0
        x = self.pos
        self.x = x[0] - 2.0
    def right(self):
        self.czy_lustro = False
        self.kat = 0
        x = self.pos
        self.x = x[0] + 2.0
class Mapa():
    def __init__(self):
        self.plansza = []
        f = open("plansza").read()
        f = f.split()
        for i in f:
            self.plansza.append(list(i))
    def kolizja(self, x, y):
        """zwraca krotkę (up,down,left,right)"""
        x=int(x//64)
        y=int(y//64)
        print(x,y)
        if y - 1 >= 0 and self.plansza [y-1][x] == "0":
            up = True
        else:
            up = False
        if y + 1 <= (len(self.plansza)) and self.plansza [y+1][x] == "0":
            down = True
        else:
            down = False
        if x - 1 >= 0 and self.plansza [y][x-1] == "0":
            left = True
        else:
            left = False
        if x + 1 <= (len(self.plansza[y])) and self.plansza[y][x+1] == "0":
            right = True
        else:
            right = False
        return(up,down,left,right)
fps = 0
gracz = Pacman(1824, 928, "pac_1")

mapa = Mapa()

def draw():
    screen.clear()
    for i in range(len(mapa.plansza)):
        for j in range(len(mapa.plansza[i])):
            if mapa.plansza [i][j] == "1":
                screen.blit("sciana", (j * 64, i * 64))
            if mapa.plansza [i][j] == "0":
                screen.blit("moneta", ((j*64)+22, (i*64)+22))
            if mapa.plansza [i][j] == "3":
                screen.blit("drzwi", (j * 64, i * 64))
            if mapa.plansza [i][j] == "5":
                screen.blit("pac_2", (j * 64, i * 64))
    gracz.draw()
def update():
    gracz.update()
    print(mapa.kolizja(gracz.pos[0],gracz.pos[1]))
    if keyboard.up:
        gracz.up()
    if keyboard.down:
        gracz.down()
    if keyboard.right:
        gracz.right()
    if keyboard.left:
        gracz.left()



pgzrun.go()