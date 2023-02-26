import numpy as np
import sys
import pygame
import math

def main():
    pygame.init()

    # Create board for game
    def create_board():
        board = np.zeros((6,7))
        return board

    # Place piece on board
    def place_piece(board, col, row, piece, screen, color, RADIUS):
        board[row][col] = piece
        pygame.draw.circle(screen, color, (int(col * SQUARE+SQUARE/2), height - int(row * SQUARE+SQUARE/2)), RADIUS)
        pygame.display.update()


    # Check if the location is on board
    def valid_location(board, col):
        return board[5][col] == 0

    # Get next row available
    def next_row(board, col):
        for row in range(ROW_COUNT):
            if board[row][col] == 0:
                return row

    # Flip board around so it looks right to viewers
    def flip_board(board):
        board = np.flip(board, 0)
        return board

    def player_score_three(board, player):
        if check_win(board, player):
            score = math.inf
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
        if check_win(board, player):
            score = math.inf
            return score
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
        if check_win(board, player):
            score = math.inf
            return score
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

    def check_win(board, piece):
        x = 3

        # Check horizontal locations right
        for r in range(ROW_COUNT):
            for c in range(COL_COUNT):
                if valid_piece(r, c+3):
                    if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                        board[r][c] = x
                        board[r][c+1] = x
                        board[r][c+2] = x
                        board[r][c+3] = x
                        return True
                else:
                    continue

        # Check horizontal locations left
        for r in range(ROW_COUNT):
            for c in range(COL_COUNT):
                if valid_piece(r, c-3):
                    if board[r][c] == piece and board[r][c-1] == piece and board[r][c-2] == piece and board[r][c-3] == piece:
                        board[r][c] = x
                        board[r][c-1] = x
                        board[r][c-2] = x
                        board[r][c-3] = x
                        return True
                else:
                    continue

        # Check vertical locations up
        for r in range(ROW_COUNT - 3):
            for c in range(COL_COUNT):
                if valid_piece(r+3, c):
                    if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                        board[r][c] = x
                        board[r+1][c] = x
                        board[r+2][c] = x
                        board[r+3][c] = x
                        return True
                else:
                    continue

        # Check vertical locations down
        for r in range(ROW_COUNT):
            for c in range(COL_COUNT):
                if valid_piece(r-3, c):
                    if board[r][c] == piece and board[r-1][c] == piece and board[r-2][c] == piece and board[r-3][c] == piece:
                        board[r][c] = x
                        board[r-1][c] = x
                        board[r-2][c] = x
                        board[r-3][c] = x
                        return True
                else:
                    continue

        # Check diagonal locations on a positive slope
        for r in range(ROW_COUNT):
            for c in range(COL_COUNT):
                if valid_piece(r+3, c+3):
                    if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                        board[r][c] = x
                        board[r+1][c+1] = x
                        board[r+2][c+2] = x
                        board[r+3][c+3] = x
                        return True
                else:
                    continue

        # Check diagonal locations on a positive slope, other direction
        for r in range(ROW_COUNT):
            for c in range(COL_COUNT):
                if valid_piece(r+3, c-3):
                    if board[r][c] == piece and board[r+1][c-1] == piece and board[r+2][c-2] == piece and board[r+3][c-3] == piece:
                        board[r][c] = x
                        board[r+1][c-1] = x
                        board[r+2][c-2] = x
                        board[r+3][c-3] = x
                        return True
                else:
                    continue

        # Check diagonal locations on a negative slope
        for r in range(ROW_COUNT):
            for c in range(COL_COUNT):
                if valid_piece(r-3, c-3):
                    if board[r][c] == piece and board[r-1][c-1] == piece and board[r-2][c-2] == piece and board[r-3][c-3] == piece:
                        board[r][c] = x
                        board[r-1][c-1] = x
                        board[r-2][c-2] = x
                        board[r-3][c-3] = x
                        return True
                else:
                    continue

        # Check diagonal locations on a negative slope, other direction
        for r in range(ROW_COUNT):
            for c in range(COL_COUNT):
                if valid_piece(r-3, c+3):
                    if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                        board[r][c] = x
                        board[r-1][c+1] = x
                        board[r-2][c+2] = x
                        board[r-3][c+3] = x
                        return True
                else:
                    continue

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

    # Define row and column count
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

    draw_board(screen, BLUE, BLACK, RADIUS)
    pygame.transform.flip(screen, True, False)
    pygame.display.update()

    board = create_board()
    game_id= ""

    # Run game as long as game is not over
    while not game_over:

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

                    # Make sure column is not full
                    if valid_location(board, col) == True:

                        # Get next available row
                        row = next_row(board, col)

                        # Place piece
                        place_piece(board, col, row, piece, screen, color, RADIUS)
                        player_one_score = 9*player_score_three(board, 1) + 4*player_score_two(board, 1) + player_score_one(board, 1)
                        print("Player 1 Score: " + str(player_one_score) + " Number of 3: " + str(player_score_three(board, 1)) + " Number of 2: " + str(player_score_two(board, 1)) + " Number of 1: " + str(player_score_one(board, 1)))
                        player_two_score = 9*player_score_three(board, 2) + 4*player_score_two(board, 2) + player_score_one(board, 2)
                        print("Player 2 Score: " + str(player_two_score) + " Number of 3: " + str(player_score_three(board, 2)) + " Number of 2: " + str(player_score_two(board, 2)) + " Number of 1: " + str(player_score_one(board, 2)))
                        game_id+=str(col)

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

                    else:
                        continue
                
                # Get player 2 input
                else:

                    # Define player 2 piece
                    piece = 2
                    player = 2
                    color = GREEN

                    x_pos = pygame.mouse.get_pos()[0]

                    col = int(math.floor(x_pos/SQUARE))

                    # Make sure column is not full
                    if valid_location(board, col) == True:

                        # Get next available rowx
                        row = next_row(board, col)

                        # Place piece
                        place_piece(board, col, row, piece, screen, color, RADIUS)
                        player_one_score = 9*player_score_three(board, 1) + 4*player_score_two(board, 1) + player_score_one(board, 1)
                        print("Player 1 Score: " + str(player_one_score) + " Number of 3: " + str(player_score_three(board, 1)) + " Number of 2: " + str(player_score_two(board, 1)) + " Number of 1: " + str(player_score_one(board, 1)))
                        player_two_score = 9*player_score_three(board, 2) + 4*player_score_two(board, 2) + player_score_one(board, 2)
                        print("Player 2 Score: " + str(player_two_score) + " Number of 3: " + str(player_score_three(board, 2)) + " Number of 2: " + str(player_score_two(board, 2)) + " Number of 1: " + str(player_score_one(board, 2)))
                        game_id+=str(col)
                        
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
                    else:
                        continue

                turn += 1
                turn = turn % 2

if __name__ == "__main__":
    main()