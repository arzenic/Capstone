import numpy as np
import sys
import pygame
import math
import copy
import timeit
import csv
import datetime

def main():
    pygame.init()

    class Node:
        def __init__(node, value, col):
            node.value = value
            node.children = []
            node.col = col

    # Create board for game
    def create_board():
        board = np.zeros((6,7))
        return board

    # Place piece on board
    def place_piece(board, col, row, piece, screen, color, RADIUS):
        board[row][col] = piece
        pygame.draw.circle(screen, color, (int(col * SQUARE+SQUARE/2), height - int(row * SQUARE+SQUARE/2)), RADIUS)
        pygame.display.update()

    def place_piece_less(temp_board, col, row, piece):
        global counter
        counter+=1
        temp_board[row][col] = piece
        return temp_board

    # Check if the location is on board
    def valid_location(board, col):
        return board[5][col] == 0

    # Get next row available
    def next_row(board, col):
        for row in range(ROW_COUNT):
            if board[row][col] == 0:
                return row
        return -1
        
        
    def set_next(node, next):
            if node.children is not None:
                node.children.append(next)

    def available_col(board):
        cols = []
        for col in range(COL_COUNT):
            if valid_location(board, col):
                cols.append(col)
        return cols
                            
    
    def mini_max(node, depth, maxPlayer, board, piece, alpha, beta):
        if ai_player == 2:
            if depth % 2 == init_depth:
                piece = 2
            else:
                piece = 1
        else:
            if depth % 2 == init_depth:
                piece = 1
            else:
                piece = 2
        bestCol = 0
        columns = available_col(board)
        if depth <= 0:
            return node.value
        if maxPlayer:
            maximum = -math.inf
            for col in columns:
                temp_board = copy.deepcopy(board)
                row = next_row(temp_board, col)

                temp_board = place_piece_less(temp_board, col, row, piece)
                score = 9*player_score_three(temp_board, ai_player) + 4*player_score_two(temp_board, ai_player) + player_score_one(temp_board, ai_player)
                alpha = max(alpha, maximum)
                if beta <= alpha:
                    break

                next = Node(score, col)
                set_next(node, next)

                if ai_player == 2:
                    if depth % 2 == init_depth:
                        piece = 2
                    else:
                        piece = 1
                else:
                    if depth % 2 == init_depth:
                        piece = 1
                    else:
                        piece = 2

                if score != math.inf and score != -math.inf:      
                    value = max(maximum, mini_max(next, depth - 1, False, temp_board, piece, alpha, beta))
                else:
                    value = score
                if value > maximum:
                    maximum = value
                    bestCol = col
                node.value = value
                node.col = bestCol
            return maximum
        else:
            minimum = math.inf
            for col in columns:
                temp_board = copy.deepcopy(board)
                row = next_row(temp_board, col)

                temp_board = place_piece_less(temp_board, col, row, piece)
                score = 9*player_score_three(temp_board, ai_player) + 4*player_score_two(temp_board, ai_player) + player_score_one(temp_board, ai_player)
                beta = min(beta, minimum)
                if beta <= alpha:
                    break
                next = Node(score, col)
                set_next(node, next)

                if ai_player == 2:
                    if depth % 2 == init_depth:
                        piece = 2
                    else:
                        piece = 1
                else:
                    if depth % 2 == init_depth:
                        piece = 1
                    else:
                        piece = 2

                if score != math.inf and score != -math.inf:      
                    value = min(minimum, mini_max(next, depth - 1, True, temp_board, piece, alpha, beta))
                else:
                    value = score
                if value < minimum:
                    minimum = value
                    bestCol = col
                node.value = value
                node.col = bestCol
            return minimum

    def check_win(board, piece):   
        for r in range(ROW_COUNT):
            for c in range(COL_COUNT):
                # Check horizontal locations right
                if valid_piece(r, c+3):
                    if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                        return True
                # Check horizontal locations left
                if valid_piece(r, c-3):
                    if board[r][c] == piece and board[r][c-1] == piece and board[r][c-2] == piece and board[r][c-3] == piece:
                        return True
                # Check vertical locations up
                if valid_piece(r+3, c):
                    if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                        return True
                # Check vertical locations down
                if valid_piece(r-3, c):
                    if board[r][c] == piece and board[r-1][c] == piece and board[r-2][c] == piece and board[r-3][c] == piece:
                        return True
                # Check diagonal locations on a positive slope
                if valid_piece(r+3, c+3):
                    if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                        return True
                # Check diagonal locations on a positive slope, other direction
                if valid_piece(r+3, c-3):
                    if board[r][c] == piece and board[r+1][c-1] == piece and board[r+2][c-2] == piece and board[r+3][c-3] == piece:
                        return True
                # Check diagonal locations on a negative slope
                if valid_piece(r-3, c-3):
                    if board[r][c] == piece and board[r-1][c-1] == piece and board[r-2][c-2] == piece and board[r-3][c-3] == piece:
                        return True
                # Check diagonal locations on a negative slope, other direction
                if valid_piece(r-3, c+3):
                    if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                        return True
    
    def player_score_three(board, player):
        if player == 1:
            opp = 2
        else:
            opp = 1
        if check_win(board, player):
            score = math.inf
            return score
        if check_win(board, opp):
            score = -math.inf
            return score
        score = 0
        total = 0
        counter = 0
        for i in range(ROW_COUNT):
            for j in range(COL_COUNT):
                if board[i][j] == player:
                    counter += 1
                    direction = ""
                    total, direction = next_piece_three(board, i, j, player, counter, direction, total)
                    score += total
                    total = 0
                    counter = 0
        return score
    
    def player_score_two(board, player):
        score = 0
        total = 0
        counter = 0
        for i in range(ROW_COUNT):
            for j in range(COL_COUNT):
                if board[i][j] == player:
                    counter += 1
                    direction = ""
                    total, direction = next_piece_two(board, i, j, player, counter, direction, total)
                    score += total
                    total = 0
                    counter = 0
        return score
    
    def player_score_one(board, player):
        score = 0
        total = 0
        for i in range(ROW_COUNT):
            for j in range(COL_COUNT):
                if board[i][j] == player:
                    total = next_piece_one(board, i, j, total)
                    score += total
                    total = 0
        return score

        
    def skip_piece(board, row, col, direction, piece):
        if "r" in direction:
            if "r-1" in direction:
                row-=1
            else:
                row += 1
        if "c" in direction:
            if "c-1" in direction:
                col -= 1
            else:
                col += 1
        if valid_piece(row, col):
            if board[row][col] == piece:
                return True
        return False

    def next_piece_three(board, row, col, piece, counter, direction, total):
        temp = direction
        direction = ""
        if len(temp) > 0:
            if "r" in temp:
                if "r-1" in temp:
                    row += -1
                    direction = "r-1"
                else:
                    row += 1
                    direction = "r1"
            if "c" in temp:
                if "c-1" in temp:
                    col -= 1
                    direction += "c-1"
                else:
                    col += 1
                    direction += "c1"
            if valid_piece(row, col):
                if board[row][col] == piece:
                    counter += 1
                    total, direction = next_piece_three(board, row, col, piece, counter, direction, total)
                elif board[row][col] == 0:
                    if counter == 3:
                        counter = 1
                        direction = ""
                        return 1, direction
                    elif counter == 2:
                        if skip_piece(board, row, col, direction, piece):
                            counter = 1
                            direction = ""
                            return 1, direction
                        else:
                            counter = 0
                            direction = ""
                            return 0, direction
                    else:
                        counter = 0
                        direction = ""
                        return 0, direction
                else:
                    direction = ""
                    counter = 0                 
                    return 0, direction
            else:
                direction = ""
                counter = 0
                return 0, direction
        else:
            for i in range(-1,2):
                for j in range(-1,2):               
                    if i == 0 and j == 0:
                            continue
                    if valid_piece(row+i, col+j):
                        if board[row+i][col+j] == piece:
                            if i != 0:
                                direction = "r" + str(i)
                            if j != 0:
                                direction += "c" + str(j)
                            if direction:
                                counter += 1
                                counter, direction = next_piece_three(board, row+i, col+j, piece, counter, direction, total)    
                                total += counter
                                counter = 1                   
        return total, direction

    def next_piece_two(board, row, col, piece, counter, direction, total):
        temp = direction
        direction = ""
        if len(temp) > 0:
            if "r" in temp:
                if "r-1" in temp:
                    row += -1
                    direction = "r-1"
                else:
                    row += 1
                    direction = "r1"
            if "c" in temp:
                if "c-1" in temp:
                    col -= 1
                    direction += "c-1"
                else:
                    col += 1
                    direction += "c1"
            if valid_piece(row, col):
                if board[row][col] == piece:
                    counter += 1
                    total, direction = next_piece_two(board, row, col, piece, counter, direction, total)
                elif board[row][col] == 0:
                    if counter == 2:
                        if "r" in temp:
                            if "r-1" in temp:
                                row += -1
                                direction = "r-1"
                            else:
                                row += 1
                                direction = "r1"
                        if "c" in temp:
                            if "c-1" in temp:
                                col -= 1
                                direction += "c-1"
                            else:
                                col += 1
                                direction += "c1"
                        if valid_piece(row, col):
                            if board[row][col] == 0:
                                counter = 1
                                direction = ""
                                return 1, direction
                    else:
                        counter = 0
                        direction = ""
                        return 0, direction
                else:
                    direction = ""
                    counter = 0                 
                    return 0, direction
            else:
                direction = ""
                counter = 0
                return 0, direction
        else:
            for i in range(-1,2):
                for j in range(-1,2):               
                    if i == 0 and j == 0:
                            continue
                    if valid_piece(row+i, col+j):
                        if board[row+i][col+j] == piece:
                            if i != 0:
                                direction = "r" + str(i)
                            if j != 0:
                                direction += "c" + str(j)
                            if direction:
                                counter += 1
                                counter, direction = next_piece_two(board, row+i, col+j, piece, counter, direction, total)    
                                total += counter
                                counter = 1                   
        return total, direction

    def next_piece_one(board, row, col, total):
        counter = 0       
        for i in range(-1,2):
            for j in range(-1,2):               
                if i == 0 and j == 0:
                        continue
                if valid_piece(row+i, col+j):
                    if board[row+i][col+j] == 0:
                        for x in range(1,3):
                            temp_i = i
                            temp_j = j
                            if i > 0:
                                temp_i = i + x
                            elif i < 0:
                                temp_i = i -x
                            if j > 0:
                                temp_j = j + x
                            elif j < 0:
                                temp_j = j -x
                            if valid_piece(row+temp_i, col+temp_j):
                                if board[row+temp_i][col+temp_j] == 0:  
                                    counter += 1
                        if counter == 2:
                            total += 1
                            counter = 0
                        else:
                            counter = 0
        return total

    # If game is won display winner
    def winning_move(player):
        pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE))
        if player == 1:
            label = winning_font.render("Player 1 Wins!", 1, RED)
        else:
            label = winning_font.render("Player 2 Wins!", 1, GREEN)
        screen.blit(label, (40,10))
        pygame.display.update()
        game_over = True
        return game_over

    # If game is drawn display message
    def draw_move():
        pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE))
        label = winning_font.render("Draw!", 1, YELLOW)
        screen.blit(label, (250,10))
        pygame.display.update()
        pygame.time.wait(3000)
        play_again()

    # Draw board on the screen for user
    def draw_board(screen, BLUE, BLACK, RADIUS):
        for r in range(ROW_COUNT):
            for c in range(COL_COUNT):
                pygame.draw.rect(screen, BLUE,(c * SQUARE, r * SQUARE + SQUARE, SQUARE, SQUARE))
                pygame.draw.circle(screen, BLACK, (int(c * SQUARE+SQUARE/2), int(r * SQUARE+SQUARE+SQUARE/2)), RADIUS)

    # Check that location for winning move is valid
    def valid_piece(r, c):
        if r < 0 or c < 0:
            return False
        else:
            try:
                board[r][c]
            except IndexError:
                return False
            else:
                return True

    # Check for a draw
    def check_draw(board):
        x = 0
        for r in range(ROW_COUNT):
            for c in range(COL_COUNT):
                if board[r][c] == 0:
                    x += 1
        if x == 0:
            return True
        return False
    
    def play_again():
        pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE * 7))
        label = winning_font.render("Play Again?", 1, WHITE)
        yes = winning_font.render("Yes", 1, WHITE)
        no = winning_font.render("No", 1, WHITE)
        screen.blit(label, (100,10))
        screen.blit(yes, (125,350))
        screen.blit(no, (475,350))
        pygame.display.update()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_pos = pygame.mouse.get_pos()[0]
                y_pos = pygame.mouse.get_pos()[1]
                if x_pos > 110 and x_pos < 275 and y_pos > 350 and y_pos < 450:
                    main()
                    break
                elif x_pos > 450 and x_pos < 575 and y_pos > 350 and y_pos < 450:
                    end_screen = True
                    break
                else:
                    continue
        return end_screen
    
    def choose_player():
        pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE * 7))
        label = choose_font.render("Choose the human player", 1, WHITE)
        p1 = choose_font.render("Player 1", 1, WHITE)
        p2 = choose_font.render("Player 2", 1, WHITE)
        screen.blit(label, (100,10))
        screen.blit(p1, (100,350))
        screen.blit(p2, (450,350))
        pygame.display.update()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_pos = pygame.mouse.get_pos()[0]
                y_pos = pygame.mouse.get_pos()[1]
                if x_pos > 95 and x_pos < 250 and y_pos > 350 and y_pos < 450:
                    ai_player = 2
                    human_player = 1
                    break
                elif x_pos > 425 and x_pos < 550 and y_pos > 350 and y_pos < 450:
                    ai_player = 1
                    human_player = 2
                    break
                else:
                    continue
        return ai_player, human_player
    
    def choose_mode():
        pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE * 7))
        label = choose_font.render("Choose playing mode", 1, WHITE)
        p1 = choose_font.render("Fo Practice", 1, WHITE)
        p2 = choose_font.render("Fo Real", 1, WHITE)
        screen.blit(label, (100,10))
        screen.blit(p1, (100,350))
        screen.blit(p2, (450,350))
        pygame.display.update()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x_pos = pygame.mouse.get_pos()[0]
                y_pos = pygame.mouse.get_pos()[1]
                if x_pos > 95 and x_pos < 250 and y_pos > 350 and y_pos < 450:
                    mode = "demo"
                    break
                elif x_pos > 425 and x_pos < 550 and y_pos > 350 and y_pos < 450:
                    mode = "prod"
                    break
                else:
                    continue
        return mode
    
    def get_user():
        #Accessed from https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame
        screen = pygame.display.set_mode(size)
        font = pygame.font.Font(None, 32)
        clock = pygame.time.Clock()
        input_box = pygame.Rect(100, 100, 140, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    if input_box.collidepoint(event.pos):
                        # Toggle the active variable.
                        active = not active
                    else:
                        active = False
                    # Change the current color of the input box.
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            if text != '':
                                return text
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            screen.fill( (0, 0, 0))
            label = choose_font.render("What is your full name", 1, WHITE)
            screen.blit(label, (100,10))
            # Render the current text.
            txt_surface = font.render(text, True, color)
            # Resize the box if the text is too long.
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            # Blit the text.
            screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            # Blit the input_box rect.
            pygame.draw.rect(screen, color, input_box, 2)

            pygame.display.flip()
            clock.tick(30)
        return text

    def end():
        pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE * 7))
        end = winning_font.render("Game Over", 1, WHITE)
        screen.blit(end, (140,275))
        pygame.display.update()
        pygame.time.wait(10000)
        game_over = True
        return game_over
    
    # Create game_over boolean which says if game is over or not and row
    game_over = False
    turn = 0

    # Define row and COL count
    ROW_COUNT = 6
    COL_COUNT = 7

    # Initialize screen for pygame
    SQUARE = 100
    RADIUS = int(SQUARE/2 - 2) 
    WIDTH = SQUARE * COL_COUNT
    HEIGHT = SQUARE * (ROW_COUNT + 1)

    size = width, height = WIDTH, HEIGHT
    BLUE = 0,0,225
    WHITE = 225,225,225
    BLACK = 0,0,0
    RED = 225,0,0
    GREEN = 0,225,0
    YELLOW = 225,225,0
    screen = pygame.display.set_mode(size)
    winning_font = pygame.font.SysFont("leelawadeeuisemilight", 65)
    choose_font = pygame.font.SysFont("leelawadeeuisemilight", 35)
    global counter
    global start_depth
    start_depth = 0
    counter = 0
    global ai_player
    global human_player
    global mode
    user = get_user()
    ai_player,human_player = choose_player()
    mode = choose_mode()
    

    draw_board(screen, BLUE, BLACK, RADIUS)
    pygame.transform.flip(screen, True, False)
    pygame.display.update()

    board = create_board()
    
    # Run game as long as game is not over
    while not game_over:
        if turn == 0 and ai_player == 2:

            # Start loop for mouse clicks and positions
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
                
                if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
                    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE))
                    if turn == 0:
                        mouse_pos = pygame.mouse.get_pos()[0]
                        pygame.draw.circle(screen, RED, (mouse_pos, int(SQUARE/2)), RADIUS)
                    else:
                        mouse_pos = pygame.mouse.get_pos()[0]
                        pygame.draw.circle(screen, GREEN, (mouse_pos, int(SQUARE/2)), RADIUS)
                    pygame.display.update()

                
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # Get player 1 input
                    if turn == 0:

                        # Define player 1 piece
                        piece = 1
                        player = 1
                        color = RED

                        x_pos = pygame.mouse.get_pos()[0]

                        col = int(math.floor(x_pos/SQUARE))

                        # Make sure COL is not full
                        if valid_location(board, col) == True:

                            # Get next available row
                            row = next_row(board, col)

                            # Place piece
                            place_piece(board, col, row, piece, screen, color, RADIUS)
                            #print(col, end = '')

                            # Check for a draw
                            if check_draw(board):
                                if mode == "prod":
                                    with open('results.csv', 'a', newline='') as f:
                                        fieldnames = ['time', 'result', 'human player', 'depth', 'user']
                                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                                        if f.tell() == 0:
                                            writer.writeheader()
                                        writer.writerow({'time':datetime.datetime.now(), 'result':"tie", 'human player':1,'depth':start_depth,'user':user})

                                draw_move()

                            # Check for a win
                            if check_win(board, 1):
                                game_over = winning_move(player)
                                

                                if mode == "prod":
                                    with open('results.csv', 'a', newline='') as f:
                                        fieldnames = ['time', 'result', 'human player', 'depth', 'user']
                                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                                        if f.tell() == 0:
                                            writer.writeheader()
                                        writer.writerow({'time':datetime.datetime.now(), 'result':"win", 'human player':1,'depth':start_depth,'user':user})
                                pygame.time.wait(3000)

                                end_screen = play_again()
                                if end_screen:
                                    game_over = end()
                            turn += 1
                            turn %= 2
                            
                    # Get player 2 input
        elif turn == 1 and ai_player == 2:
            #start = timeit.default_timer() 
            # Define player 2 piece
            piece = 2
            player = 2
            color = GREEN

            start_depth = 4
            init_depth = start_depth % 2

            col = 0
            alpha = -math.inf
            beta = math.inf
            root = Node(0, col)
                
            mini_max(root, start_depth, True, board, piece, alpha, beta)

            col = root.col

            row = next_row(board, col)
            # Place piece
            place_piece(board, col, row, piece, screen, color, RADIUS)
            print(counter)
            
            # Check for a draw
            if check_draw(board):
                if mode == "prod":
                    with open('results.csv', 'a', newline='') as f:
                        fieldnames = ['time', 'result', 'human player', 'depth', 'user']
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        if f.tell() == 0:
                            writer.writeheader()
                        writer.writerow({'time':datetime.datetime.now(), 'result':"tie", 'human player':1,'depth':start_depth,'user':user})

                draw_move()

            # Check for a win
            if check_win(board, 2):
                game_over = winning_move(player)
                if mode == "prod":
                    with open('results.csv', 'a', newline='') as f:
                        fieldnames = ['time', 'result', 'human player', 'depth', 'user']
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        if f.tell() == 0:
                            writer.writeheader()
                        writer.writerow({'time':datetime.datetime.now(), 'result':"loss", 'human player':1,'depth':start_depth,'user':user})
                pygame.time.wait(3000)
                end_screen = play_again()
                if end_screen:
                    game_over = end()

            turn += 1
            turn %= 2
            
            #stop = timeit.default_timer()

            #print('Time: ', stop - start)  
        elif turn == 0 and ai_player == 1:
            piece = 1
            player = 1
            color = RED

            start_depth = 4
            init_depth = start_depth % 2

            col = 0
            alpha = -math.inf
            beta = math.inf
            root = Node(0, col)
                
            mini_max(root, start_depth, True, board, piece, alpha, beta)

            col = root.col

            row = next_row(board, col)
            # Place piece
            place_piece(board, col, row, piece, screen, color, RADIUS)
            #print(counter)
            
            # Check for a draw
            if check_draw(board):
                if mode == "prod":
                    with open('results.csv', 'a', newline='') as f:
                        fieldnames = ['time', 'result', 'human player', 'depth', 'user']
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        if f.tell() == 0:
                            writer.writeheader()
                        writer.writerow({'time':datetime.datetime.now(), 'result':"tie", 'human player':2,'depth':start_depth,'user':user})

                draw_move()

            # Check for a win
            if check_win(board, player):
                game_over = winning_move(player)
                if mode == "prod":
                    with open('results.csv', 'a', newline='') as f:
                        fieldnames = ['time', 'result', 'human player', 'depth', 'user']
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        if f.tell() == 0:
                            writer.writeheader()
                        writer.writerow({'time':datetime.datetime.now(), 'result':"loss", 'human player':2,'depth':start_depth,'user':user})
                pygame.time.wait(3000)
                end_screen = play_again()
                if end_screen:
                    game_over = end()

            turn += 1
            turn %= 2
            
            #stop = timeit.default_timer()

            #print('Time: ', stop - start)
        elif turn == 1 and ai_player == 1:
            # Start loop for mose clicks and positions
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
                
                if event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
                    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARE))
                    mouse_pos = pygame.mouse.get_pos()[0]
                    pygame.draw.circle(screen, GREEN, (mouse_pos, int(SQUARE/2)), RADIUS)
                    pygame.display.update()

                
                if event.type == pygame.MOUSEBUTTONDOWN:

                    # Get player 1 input

                        # Define player 1 piece
                        piece = 2
                        player = 2
                        color = GREEN

                        x_pos = pygame.mouse.get_pos()[0]

                        col = int(math.floor(x_pos/SQUARE))

                        # Make sure COL is not full
                        if valid_location(board, col) == True:

                            # Get next available row
                            row = next_row(board, col)

                            # Place piece
                            place_piece(board, col, row, piece, screen, color, RADIUS)
                            #print(col, end = '')

                            # Check for a draw
                            if check_draw(board):
                                if mode == "prod":
                                    with open('results.csv', 'a', newline='') as f:
                                        fieldnames = ['time', 'result', 'human player', 'depth', 'user']
                                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                                        if f.tell() == 0:
                                            writer.writeheader()
                                        writer.writerow({'time':datetime.datetime.now(), 'result':"tie", 'human player':2,'depth':start_depth,'user':user})
                                draw_move()

                            # Check for a win
                            if check_win(board, player):
                                game_over = winning_move(player)
                                if mode == "prod":
                                    with open('results.csv', 'a', newline='') as f:
                                        fieldnames = ['time', 'result', 'human player', 'depth', 'user']
                                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                                        if f.tell() == 0:
                                            writer.writeheader()
                                        writer.writerow({'time':datetime.datetime.now(), 'result':"win", 'human player':2,'depth':start_depth,'user':user})
                                pygame.time.wait(3000)
                                end_screen = play_again()
                                if end_screen:
                                    game_over = end()
                            turn += 1
                            turn %= 2

if __name__ == "__main__":
    main()