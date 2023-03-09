""" with open('states.csv', 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['position'] == str_board:
                            col = int(row['column']) """

""" with open('states.csv', 'a', newline='') as f:
                fieldnames = ['position', 'column']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if f.tell() == 0:
                    writer.writeheader()
                writer.writerow({'position': str_board, 'column':col}) """

import numpy as np
import sys
import pygame
import math
import copy
import timeit
import csv

def main():
    pygame.init()

    # Create board for game
    def create_board():
        board = np.zeros((6,7))
        return board


    # Get next row available
    def next_row(board, col):
        for row in range(ROW_COUNT):
            if board[row][col] == 0:
                return row

    # Flip board around so it looks right to viewers
    def flip_board(board):
        board = np.flip(board, 0)
        return board
    
    def place_piece_less(temp_board, col, row, piece):
        temp_board[row][col] = piece
        return temp_board
    
    def convert_board(board):
        str_board = ""
        for row in range(ROW_COUNT):
            for col in range(COL_COUNT):
                str_board+=str(int((board[row][col])))
        return str_board
    
    def create_tree(depth, piece, board):
        if depth % 2 == init_depth:
            piece = 2
        else:
            piece = 1
        if depth != 0:
                for col in range(COL_COUNT):
                    temp_board = copy.deepcopy(board)
                    row = next_row(temp_board, col)
                    if row != -1:
                        temp_board = place_piece_less(temp_board, col, row, piece)
                        score = 9*player_score_three(temp_board, 2) + 4*player_score_two(temp_board, 2) + player_score_one(temp_board, 2)
                    str_board = convert_board(temp_board)

                    with open('scores.csv', 'a', newline='') as f:
                        fieldnames = ['position', 'score']
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        if f.tell() == 0:
                            writer.writeheader()
                        writer.writerow({'position': str_board, 'score':score}) 
                        
                    if depth % 2 == init_depth:
                        piece = 2
                    else:
                        piece = 1
                    
                    create_tree( depth - 1, piece, temp_board)

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

    def check_win(board, piece):
        # Check horizontal locations right
        for r in range(ROW_COUNT):
            for c in range(COL_COUNT):
                if valid_piece(r, c+3):
                    if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                        return True
                else:
                    continue

        # Check horizontal locations left
        for r in range(ROW_COUNT):
            for c in range(COL_COUNT):
                if valid_piece(r, c-3):
                    if board[r][c] == piece and board[r][c-1] == piece and board[r][c-2] == piece and board[r][c-3] == piece:
                        return True
                else:
                    continue

        # Check vertical locations up
        for r in range(ROW_COUNT - 3):
            for c in range(COL_COUNT):
                if valid_piece(r+3, c):
                    if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                        return True
                else:
                    continue

        # Check vertical locations down
        for r in range(ROW_COUNT):
            for c in range(COL_COUNT):
                if valid_piece(r-3, c):
                    if board[r][c] == piece and board[r-1][c] == piece and board[r-2][c] == piece and board[r-3][c] == piece:
                        return True
                else:
                    continue

        # Check diagonal locations on a positive slope
        for r in range(ROW_COUNT):
            for c in range(COL_COUNT):
                if valid_piece(r+3, c+3):
                    if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                        return True
                else:
                    continue

        # Check diagonal locations on a positive slope, other direction
        for r in range(ROW_COUNT):
            for c in range(COL_COUNT):
                if valid_piece(r+3, c-3):
                    if board[r][c] == piece and board[r+1][c-1] == piece and board[r+2][c-2] == piece and board[r+3][c-3] == piece:
                        return True
                else:
                    continue

        # Check diagonal locations on a negative slope
        for r in range(ROW_COUNT):
            for c in range(COL_COUNT):
                if valid_piece(r-3, c-3):
                    if board[r][c] == piece and board[r-1][c-1] == piece and board[r-2][c-2] == piece and board[r-3][c-3] == piece:
                        return True
                else:
                    continue

        # Check diagonal locations on a negative slope, other direction
        for r in range(ROW_COUNT):
            for c in range(COL_COUNT):
                if valid_piece(r-3, c+3):
                    if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                        return True
                else:
                    continue

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


    # Define row and column count
    ROW_COUNT = 6
    COL_COUNT = 7

    

    board = create_board()
    start = timeit.default_timer()
    depth = 7
    init_depth = depth % 2
    create_tree(depth, 2, board)
    stop = timeit.default_timer()

    print('Time: ', stop - start)  


    

if __name__ == "__main__":
    main()