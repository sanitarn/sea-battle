#Интерфейс приложения должен представлять из себя консольное окно с двумя полями 6х6
# Игрок играет с компьютером. Компьютер делает ходы наугад, но не ходит по тем клеткам, в которые он уже сходил.
# Для представления корабля опишите класс Ship с конструктором принимающим в себя набор точек (координат) на игровой доске.
# Опишите класс доски. Доска должна принимать в конструкторе набор кораблей.
# Корабли должны находится на расстоянии минимум одна клетка друг от друга.

#Корабли на доске должны отображаться следующим образом (пример)

# На каждой доске (у ИИ и у игрока) должно находится следующее количество кораблей: 1 корабль на 3 клетки, 2 корабля на 2 клетки, 4 корабля на одну клетку.
# Запретите игроку стрелять в одну и ту же клетку несколько раз. При ошибках хода игрока должно возникать исключение

# В случае, если возникают непредвиденные ситуации, выбрасывать и обрабатывать исключения.
# Буквой X помечаются подбитые корабли, буквой T — промахи.

# Побеждает тот, кто быстрее всех разгромит корабли противника.
from random import randint

class Dot ():
    """Класс отвечает за выстрел"""

    def __init__ (self, x, y):

        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self) -> str:
        return (f'Dot{self.x, self.y}')


class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self) -> str:
        return 'Вы стреляли за пределы доски'

class BoardUsedException(BoardException):
    def __str__(self) -> str:
        return 'В эту клетку вы уже стреляли'

class BoardWrongShipException(BoardException):
    pass

class Ship():
    """Класс отвечает за корабль, длина корабля, расположение и.т.д"""
    def __init__ (self, dot_nose, len_ship, horizon_or_vertic, live_ship ):        
        self.len_ship = len_ship
        self.dot_nose = dot_nose
        self.horizon_or_vertic = horizon_or_vertic
        self.live_ship = live_ship

    @property
    def dots (self):
        ship_dots = []
        for i in range(self.len_ship):
            cur_x = self.dot_nose.x
            cur_y = self.dot_nose.y

            if self.horizon_or_vertic == 0:
                cur_x+=i
            elif self.horizon_or_vertic == 1:
                cur_y+=i
            
            ship_dots.append(Dot(cur_x, cur_y))
        return ship_dots

    def shooten (self, shot):
        return shot in self.dots
            


class Board ():

    """Класс отвечает за отображение доски и кораблей на ней"""

    def __init__(self, hid = True,  size = 6 ):

        self.hid = hid
        self.size = size
        self.count = 0

        self.field = [ ['O'] * size for _ in range (size) ]
        
        self.busy = []
        self.ship = []
    
    def __str__(self):
        print ("|  1  | 2  | 3  | 4  | 5  | 6 |")
        res=""
        for i in range (self.size):
            res += '|  ' + '  | '.join (self.field[i]) + ' | \n'
            
            if self.hid == False:

                res = res.replace('O','*')

        return res

    def out(self, d):
        return not((0<= d.x < self.size) and (0<= d.y < self.size))

    def contour(self, ship, verb = False):
        near = [
            (-1, -1), (-1, 0) , (-1, 1),
            (0, -1), (0, 0) , (0 , 1),
            (1, -1), (1, 0) , (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)
    
    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = "■"
            self.busy.append(d)
        
        self.ships.append(ship)
        self.contour(ship)
    def shot(self, d):
        if self.out(d):
            raise BoardOutException()
        
        if d in self.busy:
            
            raise BoardUsedException()
        
        self.busy.append(d)
        
        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                self.field[d.x][d.y] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb = True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True
        
        self.field[d.x][d.y] = "."
        print("Мимо!")
        return False
    
    def begin(self):
        self.busy = []
class Player:
    """Класс игрока куда стрелять"""
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy
    
    def ask(self):
        raise NotImplementedError()
    
    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)

class AI(Player):
    def ask(self):
        d = Dot(randint(0,5), randint(0, 5))
        print(f"Ход компьютера: {d.x+1} {d.y+1}")
        return d

class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()
            
            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue
            
            x, y = cords
            
            if not(x.isdigit()) or not(y.isdigit()):
                print(" Введите числа! ")
                continue
            
            x, y = int(x), int(y)
            
            return Dot(x-1, y-1)


class Game:
    """ Класс отвечающий за вывод доски и игры"""
    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size = self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0,1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board
    
    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board
    def __init__(self, size = 6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True
        
        self.ai = AI(co, pl)
        self.us = User(pl, co)
    
    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")
    def loop(self):
        num = 0
        while True:
            print("-"*20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-"*20)
            print("Доска компьютера:")
            print(self.ai.board)
            print("-"*20)
            if num % 2 == 0:
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1
            
            if self.ai.board.count == 7:
                print("-"*20)
                print("Пользователь выиграл!")
                break
            
            if self.us.board.count == 7:
                print("-"*20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()

g = Game()
g.start()


