import numpy as np
import sys
import pygame
import math
import copy
from num2words import num2words
def main():
    def create_board():
            board = np.zeros((6,7))
            return board

    def flip_board(board):
        board = np.flip(board, 0)
        return board

    def next_row(board, col):
        for row in range(ROW_COUNT):
            if board[row][col] == 0:
                return row
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
       
    def place_pieces(position, board, turn):
        for x in str(position):
            x = int(x)
            row = next_row(board, x)
            if turn == 0:
                board[row][x] = 1
            else:
                board[row][x] = 2
            turn += 1
            turn %= 2
        return board
    
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

    player_one_score = 0
    ROW_COUNT = 6
    COL_COUNT = 7
    turn  = 0
    board = create_board()
    board = place_pieces(3233224456, board, turn)
    #11334434434646
    #233445510101045454

    player_one_score = player_score_two(board, 1)
    player_two_score = player_score_two(board, 2)
    print(player_one_score)
    print(player_two_score)

    board = flip_board(board)
    print(board)

if __name__ == "__main__":
    main()
