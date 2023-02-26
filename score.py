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
    def player_score(board, player):
        score = 0
        temp_counter = 0
        counter = 0
        for i in range(ROW_COUNT):
            for j in range(COL_COUNT):
                if board[i][j] == player:
                    counter += 1
                    direction = ""
                    counter = next_piece(board, i, j, player, counter, direction, temp_counter)
                    score += counter
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
        

    def next_piece(board, row, col, piece, counter, direction, temp_counter):
        temp = direction
        direction = ""
        if len(temp) > 0:
            if "r" in temp:
                if "-1" in temp:
                    row -= 1
                    direction += "r-1"
                else:
                    row += 1
                    direction = "r1"
            if "c" in temp:
                if "-1" in temp:
                    col -= 1
                    direction += "c-1"
                else:
                    col += 1
                    direction += "c1"
            if valid_piece(row, col):
                if board[row][col] == piece:
                    counter += 1
                    counter = next_piece(board, row, col, piece, counter, direction, temp_counter)
                elif board[row][col] == 0:
                    direction = ""
                    return counter
                else:
                    direction = ""
                    counter = 0                   
                    return counter
            else:
                direction = ""
                counter = 0
                return counter
        else:
            for i in range(0,2):
                for j in range(0,2):               
                    if i == 0 and j == 0:
                            continue
                    if valid_piece(row+i, col+j):
                        if board[row+i][col+j] == piece:
                            if row+i != 0 and i != 0:
                                direction = "r" + str(i)
                            if col+j != 0 and j != 0:
                                direction += "c" + str(j)
                            counter += 1
                            counter = next_piece(board, row+i, col+j, piece, counter, direction, temp_counter)    
                            temp_counter = counter
                            counter = 1                   
        return temp_counter

        
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

    player_one_score = 0
    ROW_COUNT = 6
    COL_COUNT = 7
    turn  = 0
    board = create_board()
    board = place_pieces(2233445, board, turn)

    player_one_score = player_score(board, 1)
    player_two_score = player_score(board, 2)
    print(player_one_score)
    print(player_two_score)

    board = flip_board(board)
    print(board)

if __name__ == "__main__":
    main()
