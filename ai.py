import sys # Which is useful for quit the application
import pygame
import numpy as np
import random
import copy

from constants import * # " import * "  That means import all 

screen = None
AI_score = 0
you_score = 0
class Board:
# Console Board

    def __init__(self):
        global screen
        self.squares = np.zeros((ROWS,COLS))
        self.empty_sqrs = self.squares # Squares
        self.marked_sqrs = 0
        
        
        
    
    def final_state(self , show = False):
        '''
        return 0 if there is no win yet
        return 1 if player 1 wins 
        return 2 if player 2 wins
        '''
        # Vertical Wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0 :
                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = ((col * SQSIZE + SQSIZE // 2)+80,100)
                    fPos = ((col * SQSIZE + SQSIZE // 2)+80,HEIGHT+80)
                    pygame.draw.line(screen,color,iPos,fPos,LINE_WIDTH)
                    # self.winningSound.play()
                return self.squares[0][col]
            

        # Horizontal Win
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1]== self.squares[row][2] != 0 :
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (100,(row * SQSIZE + SQSIZE // 2)+80)
                    fPos = (WIDTH+80,(row * SQSIZE + SQSIZE // 2)+80)
                    pygame.draw.line(screen,color,iPos,fPos,LINE_WIDTH)
                    # self.winningSound.play()
                    
                    
                return self.squares[row][0]

        # desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                    color = CIRC_COLOR if  self.squares[1][1] == 2 else CROSS_COLOR
                    iPos = (100,100)
                    fPos = (WIDTH +80,HEIGHT +80)
                    pygame.draw.line(screen,color,iPos,fPos,CROSS_WIDTH)
                    # self.winningSound.play()
                    
            return self.squares[1][1]

        # asc diagonal 
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                    color = CIRC_COLOR if  self.squares[1][1] == 2 else CROSS_COLOR
                    iPos = (100,HEIGHT + 60)
                    fPos = (WIDTH + 60, 100)
                    pygame.draw.line(screen,color,iPos,fPos,CROSS_WIDTH)
                    # self.winningSound.play()
                    
            return self.squares[1][1]
        
        return 0

    def mark_sqr(self,row,col,player):  
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self,row,col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row,col):
                    empty_sqrs.append((row,col))
        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0

class AI:
    def __init__(self,level = 1, player = 2): # Level 0 is basically Random AI and level 1 is basically MinMax Algorithm 
        self.level = level
        self.player = player
    
    def rnd(self,board):
        empty_sqrs  = board.get_empty_sqrs()
        idx = random.randrange(0,len(empty_sqrs))

        return empty_sqrs[idx] # (row,col)

    
    def minimax(self,board,maximizing):
        # Check terminal case
        case = board.final_state()
        # Player 1 wins
        if case == 1:
            return 1, None # eval,move

        # Player 2 wins
        if case == 2:
            return -1,None # Here player 2 is an AI so we minimize its steps
        
        # draw 
        elif board.isfull():
            return 0,None

        if maximizing:
            max_eval = -100 # any number can be provide which is less than 0 and 1
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row,col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row,col,1)
                eval = self.minimax(temp_board,False)[0]
                if eval > max_eval :
                    max_eval = eval
                    best_move = (row,col)

            return max_eval,best_move

        elif not maximizing:
            min_eval = 100 # any number can be provide which is greater than 0 and 1
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row,col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row,col,self.player)
                eval = self.minimax(temp_board,True)[0]
                if eval < min_eval :
                    min_eval = eval
                    best_move = (row,col)

            return min_eval,best_move

    def eval(self, main_board):
        if self.level == 0:
            # random choice
            eval = 'random'
            move = self.rnd(main_board)
        else:
            # MinMax Algorithm Choice
            eval,move = self.minimax(main_board,False)
        print(f'AI has chosen to mark the square in pos {move} with an eval: {eval}')

        return move # row,col
    
class Game:
    def __init__(self): # init is called every time an object is created from class
        global screen,AI_score,you_score
        self.board = Board()
        self.ai = AI()
        self.player = 2 # 1-Cross,2-Circle
        self.gamemode= 'ai' # pvp = playervs player or AI
        self.running = True 
        self.show_lines()
        self.score()
             
    def make_move(self,row,col):
           self.board.mark_sqr(row,col,self.player)
           self.draw_fig(row,col)
           self.next_turn()

    def show_lines(self):
        # BG 
        screen.fill(BG_COLOR)
        
        # HORIZONTAL_ABOVE
        pygame.draw.line(screen, LINE_COLOR, (80, 280), (680, 280), LINE_WIDTH)
        # HORIZONTAL_BELOW
        pygame.draw.line(screen, LINE_COLOR, (80, 480), (680, 480), LINE_WIDTH)
        # # #VERTICAL_LEFT
        pygame.draw.line(screen, LINE_COLOR, (280, 80), (280, 680), LINE_WIDTH)
        # VERTICAL_RIGHT
        pygame.draw.line(screen, LINE_COLOR, (480, 80), (480, 680), LINE_WIDTH)
        
    def score(self):
        global AI_score,you_score
        AI = AI_score
        You = you_score
        
        basefont = pygame.font.Font(None, 102)
        
        player1_name_display = basefont.render("AI", True, (255, 255, 255))
        screen.blit(player1_name_display, (850, 150))
        player2_name_display = basefont.render("You", True, (255, 255, 255))
        screen.blit(player2_name_display, (850, 450))

        player1_score_display = basefont.render(str(AI), True, (255, 255,255))
        screen.blit(player1_score_display, (1100, 150))
        player2_score_display = basefont.render(str(You), True, (255, 255, 255))
        screen.blit(player2_score_display, (1100, 450))
    
    def draw_fig(self,row,col):
        if self.player == 1:
    # Draw Cross
    # Draw Descending Line
           start_desc = ((col * SQSIZE + OFFSET)+80 , (row * SQSIZE + OFFSET)+80)
           end_desc = ((col * SQSIZE + SQSIZE - OFFSET)+80 , (row * SQSIZE + SQSIZE - OFFSET)+80)
           pygame.draw.line(screen,CROSS_COLOR,start_desc,end_desc,CROSS_WIDTH)
    # Draw Ascending Line
           start_asc = ((col * SQSIZE + OFFSET)+80 , (row * SQSIZE + SQSIZE - OFFSET)+80)
           end_asc = ((col * SQSIZE + SQSIZE - OFFSET)+80 , (row * SQSIZE + OFFSET)+80)
           pygame.draw.line(screen,CROSS_COLOR,start_asc,end_asc,CROSS_WIDTH)
        elif self.player == 2:
    # Draw Circles
            center = ((col * SQSIZE + SQSIZE //2)+80,(row * SQSIZE + SQSIZE // 2)+80)
            pygame.draw.circle(screen,CIRC_COLOR,center,RADIUS,CIRC_WIDTH)

    def next_turn(self):
        self.player = self.player % 2 + 1 # we can simply change the player by using this modulus operator
        # The first player plays the game the next player turn would be 2 % 2 + 1 = 1 so the next player can be played 

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

        '''if self.gamemode == 'pvp':
            self.gamemode = 'ai'
        else:
            self.gamemode = 'pvp'''

    def isover(self):
        return self.board.final_state(show = True) != 0 or self.board.isfull()
    
    def reset(self):
        self.__init__()

def main(): # this is from file gets executed
    global screen,AI_score,you_score
    # PYGAME SETUP
    pygame.init()  # Intilize the pygame
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption('TIC TAC TOE USING AI')
    screen.fill(BG_COLOR)
    clickSound = pygame.mixer.Sound('click.wav')
    winningSound = pygame.mixer.Sound('winning.wav')
    
    # object
    game = Game()
    board = game.board
    ai = game.ai

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # g-gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()

                # 0-random ai 
                if event.key == pygame.K_0:
                    ai.level = 0
                # 1-random ai
                if event.key == pygame.K_1:
                    ai.level = 1
                # r-restart 
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai


            if event.type == pygame.MOUSEBUTTONDOWN: # By clicking to find out the co-ordinates
                pos = event.pos
                row = (pos[1]-80) // 200
                col = (pos[0]-80) // 200
                if(row<3 and col<3):
                    if board.empty_sqr(row,col) and game.running:
                        game.make_move(row,col)
                        clickSound.play()
                        if game.isover():
                            if game.isover():
                                if (board.final_state(True) == 0):
                                    continue
                                else:
                                    winningSound.play()
                                    you_score += 1
                            game.running = False
                else:
                    continue              
               
            
        if game.gamemode == 'ai' and game.player == ai.player and game.running: # when the game gets completed it get crashed so for that we have add game.running
            pygame.display.update() # Update the screen

            # AI Methods
            row,col = ai.eval(board)

            game.make_move(row,col)
            clickSound.play()

            if game.isover():
                if (board.final_state(True) == 0):
                    continue
                else:
                    winningSound.play()
                    AI_score += 1
                game.running = False

               # print(event.pos)    
        pygame.display.update() # Updated color of background screen        


