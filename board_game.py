import pygame
import random

width, height = 600, 600
rows, columns = 16,16

square_size = width//columns

red = (255,105,97)
white = (255,255,255)
black = (20,20,20)
grey = (128,128,128)
blue = (59,131,189)
green = (0,255,0)
yellow = (255,255,0)
purple = (163,73,164)
brown = (128,64,0)

colors = [red,blue,green,yellow]

start_positions = [(1,1),(0,2)]
end_positions = [(2,1),(0,3)]
orientations = ['vertical', 'horizontal']

num_pieces = 4
num_objetives = 4
num_walls = 3

# crown = pygame.transform.scale(pygame.image.load('corona.png'), (45,25))



class Wall:
    def __init__(self, start_pos, end_pos, orientation):
        self.start_pos = start_pos  # Posición inicial de la pared (fila, columna)
        self.end_pos = end_pos  # Posición final de la pared (fila, columna)
        self.orientation = orientation  # Orientación de la pared: 'horizontal' o 'vertical'
        self.color = black  # Color de la pared definido previamente

    def draw(self, win):
        if self.orientation == 'horizontal':
            pygame.draw.line(win, self.color, 
                             (self.start_pos[1] * square_size, self.start_pos[0] * square_size + square_size),
                             (self.end_pos[1] * square_size , self.end_pos[0] * square_size + square_size), 5)
        elif self.orientation == 'vertical':
            pygame.draw.line(win, self.color, 
                             (self.start_pos[1] * square_size + square_size, self.start_pos[0] * square_size ),
                             (self.end_pos[1] * square_size + square_size, self.end_pos[0] * square_size ),5)

class Pieces:
    filled = 5
    edge = 0

    def __init__(self,fil,col,color):
        self.fil = fil
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = square_size * self.col + square_size // 2
        self.y = square_size * self.fil + square_size // 2
    
    def make_king(self):
        self.king = True

    def draw(self,win):
        radio = square_size//2 - self.filled
        pygame.draw.circle(win,grey,(self.x,self.y), radio + self.edge)
        pygame.draw.circle(win,self.color,(self.x,self.y), radio)
        #if self.king:
        #    win.blit(crown, (self.x - crown.get_width()//2, self.y - crown.get_height()//2))

    def move(self,fil,col):
        self.fil = fil
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)
    
class board:
    def __init__ (self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0 
        self.walls = []
        self.walls2 = []
        self.crear_board()

    def add_wall(self,start_pos,end_pos,orientation):
        self.walls.append(Wall(start_pos,end_pos,orientation))


    def draw_cuadrados(self,win):
        win.fill(white)
        for fil in range(rows):
            for col in range(fil % 2, columns, 2):
                pygame.draw.rect(win,grey,(fil*square_size, col*square_size, square_size, square_size))

    def move(self,pieza,fil,col):
        self.board[pieza.fil][pieza.col], self.board[fil][col] = self.board[fil][col], self.board[pieza.fil][pieza.col]
        pieza.move(fil,col)

        if fil == rows - 1 or fil == 0:
            pieza.make_king()
            if pieza.color == white:
                self.white_kings += 1
            else:
                self.red_kings += 1
        
    def get_pieza(self,fil,col):
        return self.board[fil][col]

    def crear_board(self):
        for fil in range(rows):
            self.board.append([])
            self.walls2.append([])
            for col in range(columns):
                self.board[fil].append(0)
                self.walls2[fil].append(0)
        
        # add the players
        i = 0
        while i < num_pieces:
            fil = random.randint(0,15)
            col = random.randint(0,15)
            if self.board[fil][col] == 0:
                color = colors[i]
                self.board[fil][col] = Pieces(fil,col,color)
                i += 1

        # add the walls
        for j in range(len(start_positions)):
            self.walls.append(Wall(start_positions[j],end_positions[j],orientations[j]))
            self.walls2[start_positions[j][0]][end_positions[j][0]] = 1
            print(self.walls)
    
    def draw(self,win):
        self.draw_cuadrados(win)
        for fil in range(rows):
            for col in range(columns):
                pieza = self.board[fil][col]
                if pieza != 0:
                    pieza.draw(win)


        for wall in self.walls:
            
            wall.draw(win)

    
    def ganador(self):
        if self.red_left <= 0:
            return white
        elif self.white_left <= 0:
            return red
        else:
            return None
    
    def get_movements_validos(self,pieza):
        movements = {}
        fil = pieza.fil
        col = pieza.col
        movements.update(self.can_move(fil,col))
        return movements


    def can_move(self,fil,col):
        movements = {}
        fil_available_izq = fil -1 
        fil_available_der = fil + 1
        col_available_up = col - 1
        col_available_down = col + 1

        if fil >= 1:
            while fil_available_izq >= 0 and self.board[fil_available_izq][col] == 0 and self.walls2[fil_available_izq][col] == 0:
                if self.walls2[fil_available_izq][col] != 0:  # Verificar pared justo al lado
                    movements[(fil_available_izq + 1, col)] = []  # Permitir estar junto a la pared
                    break
                fil_available_izq -= 1 
            if col == 0:
                movements[(fil_available_izq,col)] = []
            else:
                movements[(fil_available_izq+1,col)] = []

        if fil < 15:
            while fil_available_der <= 15 and self.board[fil_available_der][col] == 0 and self.walls2[fil_available_der][col] == 0:
                if self.walls2[fil_available_der][col] != 0:
                    movements[(fil_available_der - 1, col)] = []
                    break
                fil_available_der += 1
            movements[(fil_available_der-1,col)] = []

        if col >= 1:
            while col_available_up >= 0 and self.board[fil][col_available_up] == 0 and self.walls2[fil][col_available_up] == 0:
                if self.walls2[fil][col_available_up] != 0:
                    movements[(fil, col_available_up + 1)] = []
                    break
                col_available_up -= 1
            if fil == 0:
                movements[(fil,col_available_up)] = []
            else:
                movements[(fil,col_available_up+1)] = [] 
            
        if col < 15:
            while col_available_down <= 15 and self.board[fil][col_available_down] == 0 and self.walls2[fil][col_available_down] == 0:
                if self.walls2[fil][col_available_down] != 0:
                    movements[(fil, col_available_down - 1)] = []
                    break
                col_available_down += 1
            movements[(fil,col_available_down-1)] = []
        return movements

        # if fil >= 1:
        #     while fil_available_izq >= 0 and self.board[fil_available_izq][col] == 0 and self.walls2[fil_available_izq][col] == 0:
        #         fil_available_izq -= 1 
        #     if col == 0:
        #         movements[(fil_available_izq,col)] = []
        #     else:
        #         movements[(fil_available_izq+1,col)] = []
        # if fil < 15:
        #     while fil_available_der <= 15 and self.board[fil_available_der][col] == 0 and self.walls2[fil_available_der][col] == 0:
        #         fil_available_der += 1 
        #     movements[(fil_available_der-1,col)] = []
        # if col >= 1:
        #     while col_available_up >= 0 and self.board[fil][col_available_up] == 0 and self.walls2[fil][col_available_up] == 0:
        #         col_available_up -= 1
        #     if fil == 0:
        #         movements[(fil,col_available_up)] = []
        #     else:
        #         movements[(fil,col_available_up+1)] = [] 
            
        # if col < 15:
        #     while col_available_down <= 15 and self.board[fil][col_available_down] == 0 and self.walls2[fil][col_available_down] == 0:
        #         col_available_down += 1 
        #     movements[(fil,col_available_down-1)] = []
        # return movements    

    # def can_move(self,fil,col):
    #     movements = {}
    #     fil_available_izq = fil -1 
    #     fil_available_der = fil + 1
    #     col_available_up = col - 1
    #     col_available_down = col + 1

    #     if fil > 1:
    #         while fil_available_izq > 0 and self.board[fil_available_izq-1][col] == 0 and self.walls2[fil_available_izq][col] == 0:
    #             fil_available_izq -= 1 
    #         movements[(fil_available_izq,col)] = []
    #     if fil < 15:
    #         while fil_available_der < 15 and self.board[fil_available_der+1][col] == 0 and self.walls2[fil_available_der][col] == 0:
    #             fil_available_der += 1 
    #         movements[(fil_available_der,col)] = []
    #     if col > 1:
    #         while col_available_up > 0 and self.board[fil][col_available_up-1] == 0 and self.walls2[fil][col_available_up] == 0:
    #             col_available_up -= 1 
    #         movements[(fil,col_available_up)] = []
    #     if col < 15:
    #         while col_available_down < 15 and self.board[fil][col_available_down+1] == 0 and self.walls2[fil][col_available_down] == 0:
    #             col_available_down += 1 
    #         movements[(fil,col_available_down)] = []
    #     return movements    

    


 
    
class Juego:
    def __init__(self,win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.draw_movements_validos(self.movements_validos)
        pygame.display.update()
    
    def _init(self):
        self.selected = None
        self.board = board()
        self.movements_validos = {}

    def ganador(self):
        return self.board.ganador()
    
    def reset(self):
        self._init()

    def select(self,fil,col):
        if self.selected:
            result = self._move(fil,col)
            if not result:
                self.selected = None
                self.select(fil,col)

        pieza = self.board.get_pieza(fil,col)
        if pieza != 0:
            self.selected = pieza
            self.movements_validos = self.board.get_movements_validos(pieza)
            return True
        return False
    
    def _move(self,fil,col):
        pieza = self.board.get_pieza(fil,col)
        if self.selected and pieza == 0 and (fil,col) in self.movements_validos:
            self.board.move(self.selected, fil, col)
            skipped = self.movements_validos[(fil,col)]
            if skipped:
                self.board.eliminar(skipped)
        else:
            return False
        return True
    
    def draw_movements_validos(self,movements):
        for move in movements:
            fil, col = move
            pygame.draw.circle(self.win, purple, (col*square_size + square_size//2, fil*square_size + square_size//2), 15)




fps = 60
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('game')


def get_fil_col_from_mouse(pos):
    x,y = pos
    fil = y // square_size
    col = x // square_size
    return fil,col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Juego(win)

    while run:
        clock.tick(fps)
        if game.ganador() != None:
            print(game.ganador())
            run = False


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                fil, col = get_fil_col_from_mouse(pos)
                game.select(fil,col)
        game.update()
    pygame.quit()
main()
