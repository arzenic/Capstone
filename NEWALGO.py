import numpy as np
import sys
import pygame
import math
import copy
import timeit
import csv

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
    
    def flip_board(board):
        board = np.flip(board, 0)
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
        if depth % 2 == init_depth:
            piece = 2
        else:
            piece = 1
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
                score = 9*player_score_three(temp_board, 2) + 4*player_score_two(temp_board, 2) + player_score_one(temp_board, 2)
                alpha = max(alpha, maximum)
                if beta <= alpha:
                    break
                next = Node(score, col)
                set_next(node, next)

                if (depth) % 2 == init_depth:
                        piece = 2
                else:
                    piece = 1

                value = max(maximum, mini_max(next, depth - 1, False, temp_board, piece, alpha, beta))
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
                score = 9*player_score_three(temp_board, 2) + 4*player_score_two(temp_board, 2) + player_score_one(temp_board, 2)
                beta = min(beta, minimum)
                if beta <= alpha:
                    break
                next = Node(score, col)
                set_next(node, next)

                if (depth) % 2 == init_depth:
                    piece = 2
                else:
                    piece = 1

                value = min(minimum, mini_max(next, depth - 1, True, temp_board, piece, alpha, beta))
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
    winning_font = pygame.font.SysFont("monospace", 75)
    global counter
    counter = 0

    draw_board(screen, BLUE, BLACK, RADIUS)
    pygame.transform.flip(screen, True, False)
    pygame.display.update()

    board = create_board()

    # Run game as long as game is not over
    while not game_over:
        if turn == 0:

            # Start loop for mose clicks and positions
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
                                draw_move()

                            # Check for a win
                            if check_win(board, 1):
                                game_over = winning_move(player)
                                pygame.time.wait(3000)
                                end_screen = play_again()
                                if end_screen:
                                    game_over = end()
                        turn += 1
                        turn %= 2
                    
                    # Get player 2 input
        if turn == 1:
            #start = timeit.default_timer() 
            # Define player 2 piece
            piece = 2
            player = 2
            color = GREEN

            global start_depth
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
                draw_move()

            # Check for a win
            if check_win(board, 2):
                game_over = winning_move(player)
                pygame.time.wait(3000)

                end_screen = play_again()
                if end_screen:
                    game_over = end()

            turn += 1
            turn %= 2
            
            #stop = timeit.default_timer()

            #print('Time: ', stop - start)  

if __name__ == "__main__":
    main()