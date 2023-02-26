
def main():
    class Node:
        def __init__(node, value):
            node.value = value
            node.children = []

    def set_value(node, value):
            node.value = value
        
    def set_next(node, next):
            node.children.append(next)
    
    def print_tree(node, depth):
        if node is not None and depth != 0:
            print(node.value)
            for i in node.children:
                print_tree(i, depth - 1)


    def create_tree(node, depth, piece, board):
        if depth != 0:
            for col in range(COL_COUNT):
                temp_board = copy.deepcopy(board)
                row = next_row(temp_board, col)
                if row != -1:
                    temp_board = place_piece_less(temp_board, col, row, piece)
                    score = 9*player_score_three(temp_board, piece) + 4*player_score_two(temp_board, piece) + player_score_one(temp_board, piece)
                    next = Node(score)
                    set_next(node, next)
                    if piece % 2 == parity:
                        piece = 1
                    else:
                        piece = 2
                    create_tree(next, depth - 1, piece, temp_board)

    my_node = Node(10)
    create_tree(my_node, 3)
    print_tree(my_node, 3)



if __name__ == "__main__":
    main()




