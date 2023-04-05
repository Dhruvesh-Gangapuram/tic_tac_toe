import pygame
import tkinter
import socket
import tkinter as tk
import numpy as np
import threading

pygame.init()

client_win = None
server_win = None
screen = None
win_size = None
gameover = False
LINE_WIDTH = 15
LINE_COLOR = (23, 145, 135)
player_1 = [' ', 0]
player_2 = [' ', 0]
basefont = pygame.font.Font(None, 102)
smallfont = pygame.font.Font(None, 22)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 25
CROSS_WIDTH = 30
SPACE = 55
board = np.zeros((BOARD_ROWS, BOARD_COLS))
player = 1
myfont = ("Comic Sans MS", 32, "bold")
P1_score = 0
P2_score = 0



def marksquare(row, col, player):
    global board
    new_board = board.copy()
    new_board[row][col] = player
    board = new_board

def available_square(row, col):
    return board[row][col] == 0

def is_board_full():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False
            else:
                return True

def draw_figure():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, (int((col * 200 + 200/2) + 80), int((row * 200 + 200/2)+80)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, CROSS_COLOR, ((col * 200 + SPACE)+80, (row * 200 + 200 - SPACE)+80),
                                    ((col * 200 + 200 - SPACE)+80, (row * 200 + SPACE)+80), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, ((col * 200 + SPACE)+80, (row * 200 + SPACE)+80),
                                    ((col * 200 + 200 - SPACE)+80, (row * 200 + 200 - SPACE)+80), CROSS_WIDTH)

def check_winner(player):
    # vertical win check
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_win_line(col, player)
            # time.sleep(1)
            return True

    # horzontal win check
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_win_line(row, player)
            return True

    # ace diagonal
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_asc_diagonal_win_line(player)
        return True

    # dec diagonal
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_dec_diagonal_win_line(player)
        return True

    return False

def draw_vertical_win_line(col, player):
    global win_size
    posX = col * 200 + 100 + 80

    if player == 1:
        Color = CIRCLE_COLOR
    elif player == 2:
        Color = CROSS_COLOR

    pygame.draw.line(screen, Color, (posX, 95),
                        (posX, win_size[1] - 95), 15)

def draw_horizontal_win_line(row, player):
    posY = row * 200 + 100 + 80

    if player == 1:
        Color = CIRCLE_COLOR
    elif player == 2:
        Color = CROSS_COLOR

    pygame.draw.line(screen, Color, (95, posY), (680 - 15, posY), 15)

def draw_asc_diagonal_win_line(payer):
    if player == 1:
        Color = CIRCLE_COLOR
    elif player == 2:
        Color = CROSS_COLOR

    pygame.draw.line(screen, Color, (80, 680), (680, 80), 15)

def draw_dec_diagonal_win_line(player):
    if player == 1:
        Color = CIRCLE_COLOR
    elif player == 2:
        Color = CROSS_COLOR

    pygame.draw.line(screen, Color, (115, 115), (650, 650), 15)

def restart():
    global board
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen.fill(BG_COLOR)
    game()
    player = 1
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            new_board = board.copy()
            new_board[row][col] = 0
            board = new_board
def send():
    global server_win
    # main_win.destroy()
    server_win = tk.Tk()
    server_win.attributes("-fullscreen", True)
    server_win['background'] = "#1CAA9C"
    server_win.title("server")
    # getting ip address
    ipaddress = socket.gethostbyname(socket.gethostname())

    iplabel = tk.Label(server_win, text=ipaddress, bg="#1CAA9C")
    iplabel.configure(font=myfont)
    iplabel.pack(anchor="center")
    # server()
    threading.Thread(target=handle_connections).start()

def handle_connections():
    
    global gameover, board, player, P1_score, P2_score
    server_socket = socket.socket()
    host = socket.gethostname()
    port = 4442
    server_socket.bind((host, port))
    server_socket.listen(1)
    client, address = server_socket.accept()

    game()
    running = True
    while running:
        if player == 1:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_RETURN:
                        restart()
                        response = board
                        client.sendall(response)
                        player = 2
                        gameover = False
                if event.type == pygame.MOUSEBUTTONDOWN and not gameover:
                    mouseX = event.pos[0]
                    mouseY = event.pos[1]
                    click_row = int((mouseY-80) // 200)
                    click_col = int((mouseX-80) // 200)
                    if (click_col < 3 and click_row < 3):
                        clicked_col = click_col
                        clicked_row = click_row
                    else:
                        continue
                    if available_square(clicked_row, clicked_col):
                        marksquare(clicked_row, clicked_col, player) 
                        if check_winner(player):
                            gameover = True
                            P1_score += 1
                        player = 2
                        response = board
                        client.sendall(response)
        elif player == 2:
            response = client.recv(1024)
            martix_response = np.frombuffer(response, dtype=np.float64)
            if len(martix_response) != 0:
                board = martix_response.reshape((3, 3))
            else:
                continue
            if check_winner(player):
                gameover = True
                P2_score += 1
            draw_figure()
            
            player = 1
        draw_figure()
        pygame.display.update()
    client.close()

def game():
    global screen, P1_score, P2_score,win_size
    player1 = P1_score
    player2 = P2_score
    screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

    screen.fill(BG_COLOR)
    # screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    pygame.display.set_caption("Server")

    win_size = pygame.display.get_window_size()
    # HORIZONTAL_ABOVE
    pygame.draw.line(screen, LINE_COLOR, (80, 280), (680, 280), LINE_WIDTH)
    # HORIZONTAL_BELOW
    pygame.draw.line(screen, LINE_COLOR, (80, 480), (680, 480), LINE_WIDTH)
    # # #VERTICAL_LEFT
    pygame.draw.line(screen, LINE_COLOR, (280, 80), (280, 680), LINE_WIDTH)
    # VERTICAL_RIGHT
    pygame.draw.line(screen, LINE_COLOR, (480, 80), (480, 680), LINE_WIDTH)

    basefont = pygame.font.Font(None, 102)
        
    player1_name_display = basefont.render("Player 1", True, (255, 255, 255))
    screen.blit(player1_name_display, (850, 150))
    player2_name_display = basefont.render("Player 2", True, (255, 255, 255))
    screen.blit(player2_name_display, (850, 450))

    player1_score_display = basefont.render(str(player1), True, (255, 255,255))
    screen.blit(player1_score_display, (1300, 150))
    player2_score_display = basefont.render(str(player2), True, (255, 255, 255))
    screen.blit(player2_score_display, (1300, 450))
