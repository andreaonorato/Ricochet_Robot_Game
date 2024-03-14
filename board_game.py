import pygame
import random
import copy

# Constants
GRID_SIZE = 8
CELL_SIZE = 50
WIN_SIZE = GRID_SIZE * CELL_SIZE
ROBOT_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
TARGET_COLOR = (255, 0, 0)
WALL_COLOR = (255, 255, 0)
BG_COLOR = (0, 0, 0)

class Square:
    def __init__(self, x, y, walls):
        self.x = x # position x of the square
        self.y = y # position y of the square
        self.walls = {'n': False, 's': False, 'e': False, 'w': False} # walls=false means that there is no wall
        self.occupied_by = None # None when it is empty, Robot number when it contains a robot
        self.is_goal = None # flag that states if it is a goal

    def drawSquare(self, win):
        rect = pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(win, (255, 255, 255), rect, 1)

        # Draw walls based on self.walls
        wall_thickness = 5  # Adjust this value for desired wall thickness
        if self.walls['n']:
            pygame.draw.line(win, WALL_COLOR, (rect.left, rect.top), (rect.right, rect.top), wall_thickness)
        if self.walls['s']:
            pygame.draw.line(win, WALL_COLOR, (rect.left, rect.bottom), (rect.right, rect.bottom), wall_thickness)
        if self.walls['e']:
            pygame.draw.line(win, WALL_COLOR, (rect.right, rect.top), (rect.right, rect.bottom), wall_thickness)
        if self.walls['w']:
            pygame.draw.line(win, WALL_COLOR, (rect.left, rect.top), (rect.left, rect.bottom), wall_thickness)

        if self.occupied_by is not None:
            color = ROBOT_COLORS[self.occupied_by]
            pygame.draw.circle(win, color, (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
        else: 
            pygame.draw.circle(win, (0,0,0), (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
        
        if self.is_goal:
            pygame.draw.rect(win, TARGET_COLOR, rect)

    def add_robot(self, r):
        self.occupied_by = r

    def remove_robot(self):
        self.occupied_by = None
    
    def add_wall(self, walls):
        self.walls = walls

    def add_goal(self):
        self.is_goal = True

    def is_occupied(self, name_robot):
        if self.occupied_by!=name_robot and self.occupied_by is not None:
            return True
        else: return False
       # return self.occupied_by

    def get_wall(self,direction):
        return self.walls[direction]
    

    

class State: # State is a state
    def __init__(self):
        self.grid = [] 
        self.walls = []
        self.robots = {} # map robot int as key, coordinates as value
        #self.goal = {} # map goal int as key, coordinates as value, the game usually have only one goal
        self.ParentState = None
        for y in range(GRID_SIZE):
            row = []
            for x in range(GRID_SIZE):
                row.append(Square(x, y, self.walls))
            self.grid.append(row)
        # square in 0,0
       # s = self.grid[0][0]
        #self.populate_board()

    def draw(self, win):
        for row in self.grid:
            for square in row:
                square.drawSquare(win)
    
    def setParentState(self, ParentState):
        self.ParentState = ParentState

    def populate_board(self):
        # add a robot in square 0,0 and some walls
        s_wall11 = {'n': False, 's': True, 'e': False, 'w': False}
        s_wall12 = {'n': True, 's': False, 'e': False, 'w': False}
        s_wall21 = {'n': False, 's': False, 'e': True, 'w': False}
        s_wall22 = {'n': False, 's': False, 'e': False, 'w': True}
        self.grid[1][1].add_wall(s_wall11)
        self.grid[2][1].add_wall(s_wall12)
        self.grid[2][2].add_wall(s_wall21)
        self.grid[2][3].add_wall(s_wall22)
        #print("Created robot "+str(r.getName()))
        self.grid[2][4].add_robot(2)
        self.grid[0][0].add_robot(1)
        self.robots[2] = (4,2)
        self.robots[1] = (0,0)
        # define the goal
        #self.goal[1] = (7,7)
        self.grid[7][7].add_goal()
    
    def populate_board2(self):
        # add a robot in square 0,0 and some walls
        s_wall11 = {'n': False, 's': True, 'e': False, 'w': False}
        s_wall12 = {'n': True, 's': False, 'e': False, 'w': False}
        s_wall21 = {'n': False, 's': False, 'e': True, 'w': False}
        s_wall22 = {'n': False, 's': False, 'e': False, 'w': True}
        self.grid[1][1].add_wall(s_wall11)
        self.grid[2][1].add_wall(s_wall12)
        self.grid[2][2].add_wall(s_wall21)
        self.grid[5][4].add_wall(s_wall22)
        self.grid[3][3].add_robot(2)
        self.grid[0][0].add_robot(1)
        self.robots[2] = (3,3)
        self.robots[1] = (0,0)
    
    def getSquare(self, x, y):
        return self.grid[x][y]
    
    def you_won(self): # check robot position is in goal
        pass
        '''for robot_n, robot_pos in self.robots.items():
            if robot_pos == pos:
                print("This is robot",robot_n," pos: ",robot_pos[0], robot_pos[1])
                return robot_n
        return None '''
    
    def move_robot(self, selected_robot, direction):
        y, x = self.robots[selected_robot]
        print("I am robot ",selected_robot, " in position",x,y, "and I want to move ",direction)
        self.grid[x][y].remove_robot()
        if direction == 'n':
            while x>=0 and self.grid[x][y].get_wall(direction)!=True:
                if x==0: break
                x -= 1
                # check that the place is not occupied by another robot already
                if self.grid[x][y].is_occupied(selected_robot):
                    x += 1
                    break
        elif direction == 's':
            while x<=7 and self.grid[x][y].get_wall(direction)!=True:
                if x==7: break
                x += 1
                if self.grid[x][y].is_occupied(selected_robot):
                    x -= 1
                    break
        elif direction == 'w':
            while y>=0 and self.grid[x][y].get_wall(direction)!=True:
                if y==0: break
                y -=1
                if self.grid[x][y].is_occupied(selected_robot):
                    y += 1
                    break
        elif direction == 'e':
            while y<=7 and self.grid[x][y].get_wall(direction)!=True:
                if y==7: break
                y += 1
                if self.grid[x][y].is_occupied(selected_robot):
                    y -= 1
                    break

        self.grid[x][y].add_robot(selected_robot)
        
        self.robots[selected_robot] = (y,x)

    def get_robot_from_pos(self, pos):
        for robot_n, robot_pos in self.robots.items():
            if robot_pos == pos:
                print("This is robot",robot_n," pos: ",robot_pos[0], robot_pos[1])
                return robot_n
        return None
        

class Game:
    def __init__(self):
        self.states = []
        self.states.append(State())

    def launch_game(self):
        pygame.init()
        win = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))
        pygame.display.set_caption("Ricochet Robots")
        clock = pygame.time.Clock()
        state_number = 0
        selected_robot = None
  
        print("You are in state: "+str(state_number))
        running = True
        while running:
            win.fill(BG_COLOR)
            self.states[state_number].draw(win) # Draw empty board, initial state

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_SPACE: # Start/Reset the game
                        state_number += 1
                        print("You are in state: "+str(state_number))
                        self.states.append(State())
                        self.states[state_number].populate_board()

                    elif event.key == pygame.K_UP and selected_robot: # Go up
                        state_number += 1
                        print("You are in state: "+str(state_number))
                        self.states.append(copy.deepcopy(self.states[state_number-1])) # Copy the parent state in the new state
                        # Deep copy
                        self.states[state_number].setParentState(self.states[state_number-1])
                        self.states[state_number].move_robot(selected_robot,'n')
                        # I should check that the robot move (check robot position this_state!=parent_state), because if it did not it does not count as new state
                        #self.states[state_number].populate_board()
                        
                    elif event.key == pygame.K_DOWN and selected_robot:
                        state_number += 1
                        print("You are in state: "+str(state_number))
                        self.states.append(copy.deepcopy(self.states[state_number-1])) # Copy the parent state in the new state
                        self.states[state_number].setParentState(self.states[state_number-1])
                        self.states[state_number].move_robot(selected_robot,'s')
                        #self.states[state_number].populate_board2()

                    elif event.key == pygame.K_RIGHT and selected_robot:
                        state_number += 1
                        print("You are in state: "+str(state_number))
                        self.states.append(copy.deepcopy(self.states[state_number-1])) # Copy the parent state in the new state
                        self.states[state_number].setParentState(self.states[state_number-1])
                        self.states[state_number].move_robot(selected_robot,'e')
                    
                    elif event.key == pygame.K_LEFT and selected_robot:
                        state_number += 1
                        print("You are in state: "+str(state_number))
                        self.states.append(copy.deepcopy(self.states[state_number-1])) # Copy the parent state in the new state
                        self.states[state_number].setParentState(self.states[state_number-1])
                        self.states[state_number].move_robot(selected_robot,'w')

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    grid_pos = (mouse_pos[0] // GRID_SIZE//6, mouse_pos[1] // GRID_SIZE//6)
                    #print(grid_pos[0],grid_pos[1]) # Position
                    selected_robot = self.states[state_number].get_robot_from_pos(grid_pos)
                    if selected_robot: print("Selected robot: ",selected_robot)
                    else: print("You need to select a robot")

            pygame.display.flip()
            clock.tick(60)

            # Here we check the goal
            if self.states[state_number].you_won():
                print("YOU WIN!!!")
                pygame.time.wait(3000)  # Wait for 2 seconds before closing the game
                break        

        pygame.quit()

# Launch the game
game = Game()
game.launch_game()
