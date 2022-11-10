
import random
from time import *


class PlainPiece:
    '''Class containing the plain pieces and its associated methods.'''

    # All dictionaries has 1 and 2 as keys which represents player 1 and player 2

    # If a piece can make another jump move, its coordinates will be appended to this list
    jump_again_list = []

    # Stores the coordinates of each piece that can make a jump move. Used only for the AI-moves
    AI_check_jump_moves_dict = {1: [], 2: []}

    # Stores the coordinates of each piece that can make a move. Used only for the AI-moves
    AI_check_moves_dict = {1: [], 2: []}

    # Contains the current positions of each regular piece
    pieces_dict = {1: [], 2: []}

    # Contains the current positions of each king piece
    king_pieces_dict = {2: [], 1: []}

    # The amount of squares on one side of the quadratic board
    board_size_list = [8]

    def __init__(self, x_pos, y_pos, player):
        '''Creates a new piece.

        :param x_pos: Current x-coordinate of the piece
        :param y_pos: Current y-coordinate of the piece
        :param player: Which player the piece belongs to
        '''

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.player = player
        self.valid_moves_list = []
        self.valid_jump_moves_list = []

    def check_if_empty_square(self, x_square, y_square):
        '''Checks if a square diagonally from the piece is empty.

        :param x_square: The x-coordinate of the square you want to check relative to the piece's position
        :param y_square: The y-coordinate of the square you want to check relative to the piece's position
        :return: Boolean variable. True if the square is empty. False if the square contains another piece
        '''

        if [x_square, y_square] not in PlainPiece.pieces_dict[1] \
                and [x_square, y_square] not in PlainPiece.king_pieces_dict[1]:
            if [x_square, y_square] not in PlainPiece.pieces_dict[2] \
                    and [x_square, y_square] not in PlainPiece.king_pieces_dict[2]:
                return True
        return False

    def check_if_opponent_on_square(self, x_square, y_square):
        '''Checks if the opponents piece is on a square and adds it to the "valid jump moves"-list if that is the case.

        :param x_square: The x-coordinate of the square you want to check relative to the piece's position
        :param y_square: The y-coordinate of the square you want to check relative to the piece's position
        :return: (nothing)
        '''

        if self.player == 1:
            if [x_square, y_square] in PlainPiece.pieces_dict[2] or [x_square, y_square] in \
                    PlainPiece.king_pieces_dict[2]:
                return True
        elif self.player == 2:
            if [x_square, y_square] in PlainPiece.pieces_dict[1] or [x_square, y_square] in \
                    PlainPiece.king_pieces_dict[1]:
                return True
        return False

    def remove_captured_piece(self, x, y):
        '''Removes the captured piece from the dictionary.

        :param x: The x-coordinate of the captured piece relative to the new position of the capturing piece
        :param y: The y-coordinate of the captured piece relative to the new position of the capturing piece
        :return: (nothing)
        '''

        if self.player == 1:
            if [x, y] in PlainPiece.pieces_dict[2]:
                PlainPiece.pieces_dict[2].remove([x, y])
                return
            elif [x, y] in PlainPiece.king_pieces_dict[2]:
                PlainPiece.king_pieces_dict[2].remove([x, y])
                return
        elif self.player == 2:
            if [x, y] in PlainPiece.pieces_dict[1]:
                PlainPiece.pieces_dict[1].remove([x, y])
                return
            elif [x, y] in PlainPiece.king_pieces_dict[1]:
                PlainPiece.king_pieces_dict[1].remove([x, y])
                return

    def check_which_piece_captured(self, new_x, new_y):
        '''Checks which piece that has been captured.

        :param new_x: The new x-coordinate of the piece
        :param new_y: The new y-coordinate of the piece
        :return: (nothing)
        '''

        if [new_x - 2, new_y + 2] == [self.x_pos, self.y_pos]:
            self.remove_captured_piece(new_x - 1, new_y + 1)
            return
        elif [new_x + 2, new_y + 2] == [self.x_pos, self.y_pos]:
            self.remove_captured_piece(new_x + 1, new_y + 1)
            return
        elif [new_x - 2, new_y - 2] == [self.x_pos, self.y_pos]:
            self.remove_captured_piece(new_x - 1, new_y - 1)
            return
        elif [new_x + 2, new_y - 2] == [self.x_pos, self.y_pos]:
            self.remove_captured_piece(new_x + 1, new_y - 1)
            return

    def valid_moves(self):
        '''Checks all the valid moves the piece can make and adds them to a list.

        :return: The list containing all valid moves
        '''

        # Checks every square diagonally around the piece to see if any other piece is there
        if self.check_if_empty_square(self.x_pos + 1, self.y_pos + 1):
            if self.player == 2:
                if self.x_pos + 1 < PlainPiece.board_size_list[0] and self.y_pos + 1 < PlainPiece.board_size_list[0]:
                    self.valid_moves_list.append([self.x_pos + 1, self.y_pos + 1])

        if self.check_if_empty_square(self.x_pos - 1, self.y_pos + 1):
            if self.player == 2:
                if self.x_pos - 1 >= 0 and self.y_pos + 1 < PlainPiece.board_size_list[0]:
                    self.valid_moves_list.append([self.x_pos - 1, self.y_pos + 1])

        if self.check_if_empty_square(self.x_pos + 1, self.y_pos - 1):
            if self.player == 1:
                if self.x_pos + 1 < PlainPiece.board_size_list[0] and self.y_pos - 1 >= 0:
                    self.valid_moves_list.append([self.x_pos + 1, self.y_pos - 1])

        if self.check_if_empty_square(self.x_pos - 1, self.y_pos - 1):
            if self.player == 1:
                if self.x_pos - 1 >= 0 and self.y_pos - 1 >= 0:
                    self.valid_moves_list.append([self.x_pos - 1, self.y_pos - 1])

        return self.valid_moves_list

    def valid_jump_moves(self):
        '''Checks all the valid jump moves the piece can make and adds them to a list.

        :return: A list containing all the possible jump moves
        '''

        # Checks if the jumping position is inside the board
        if self.player == 2:
            if self.x_pos + 2 < PlainPiece.board_size_list[0] and self.y_pos + 2 < PlainPiece.board_size_list[0]:
                if self.check_if_empty_square(self.x_pos + 2, self.y_pos + 2):
                    # Checks if a piece of the opponent is between the starting position and the jumping position
                    if self.check_if_opponent_on_square(self.x_pos + 1, self.y_pos + 1):
                        self.valid_jump_moves_list.append([self.x_pos + 2, self.y_pos + 2])

            if self.x_pos - 2 >= 0 and self.y_pos + 2 < PlainPiece.board_size_list[0]:
                if self.check_if_empty_square(self.x_pos - 2, self.y_pos + 2):
                    if self.check_if_opponent_on_square(self.x_pos - 1, self.y_pos + 1):
                        self.valid_jump_moves_list.append([self.x_pos - 2, self.y_pos + 2])

        elif self.player == 1:
            if self.x_pos + 2 < PlainPiece.board_size_list[0] and self.y_pos - 2 >= 0:
                if self.check_if_empty_square(self.x_pos + 2, self.y_pos - 2):
                    if self.check_if_opponent_on_square(self.x_pos + 1, self.y_pos - 1):
                        self.valid_jump_moves_list.append([self.x_pos + 2, self.y_pos - 2])

            if self.x_pos - 2 >= 0 and self.y_pos - 2 >= 0:
                if self.check_if_empty_square(self.x_pos - 2, self.y_pos - 2):
                    if self.check_if_opponent_on_square(self.x_pos - 1, self.y_pos - 1):
                        self.valid_jump_moves_list.append([self.x_pos - 2, self.y_pos - 2])

        return self.valid_jump_moves_list

    def move_piece(self, new_x, new_y):
        '''Checks if the move is valid, removes the old position from the pieces dictionary and adds the new position.

        :param new_x: The x-coordinate of the new square you want the piece to move to
        :param new_y: The y-coordinate of the new square you want the piece to move to
        :return: (nothing)
        '''

        # Checks if the piece is in the player's dictionary
        if [self.x_pos, self.y_pos] in PlainPiece.pieces_dict[self.player]:
            if [new_x, new_y] in self.valid_moves():
                # Checks if the player can make a jump move
                if not check_jump_moves(self.player):
                    # If a piece has reached the other side it gets appended to the king_piece_dict
                    if self.player == 1 and new_y == 0:
                        PlainPiece.king_pieces_dict[self.player].append([new_x, new_y])
                        PlainPiece.pieces_dict[self.player].remove([self.x_pos, self.y_pos])
                    elif self.player == 2 and new_y == PlainPiece.board_size_list[0] - 1:
                        PlainPiece.king_pieces_dict[self.player].append([new_x, new_y])
                        PlainPiece.pieces_dict[self.player].remove([self.x_pos, self.y_pos])
                    else:
                        PlainPiece.pieces_dict[self.player].append([new_x, new_y])
                        PlainPiece.pieces_dict[self.player].remove([self.x_pos, self.y_pos])
                        PlainPiece.AI_check_moves_dict[self.player].clear()
                        PlainPiece.AI_check_jump_moves_dict[self.player].clear()
                else:
                    raise EnvironmentError("You must take a piece if you can!")
            elif [new_x, new_y] in self.valid_jump_moves():
                self.check_which_piece_captured(new_x, new_y)
                if self.player == 1 and new_y == 0:
                    PlainPiece.king_pieces_dict[self.player].append([new_x, new_y])
                elif self.player == 2 and new_y == PlainPiece.board_size_list[0] - 1:
                    PlainPiece.king_pieces_dict[self.player].append([new_x, new_y])
                else:
                    PlainPiece.pieces_dict[self.player].append([new_x, new_y])
                # Checks if the newly moved piece has any legal jump moves
                if PlainPiece(new_x, new_y, self.player).valid_jump_moves():
                    PlainPiece.jump_again_list.clear()
                    PlainPiece.jump_again_list.append([new_x, new_y])
                else:
                    PlainPiece.jump_again_list.clear()
                PlainPiece.pieces_dict[self.player].remove([self.x_pos, self.y_pos])
                PlainPiece.AI_check_moves_dict[self.player].clear()
                PlainPiece.AI_check_jump_moves_dict[self.player].clear()
            else:
                raise ValueError("That is not a valid move!")
        else:
            raise TypeError("You must select a piece of your own!")
        return


class KingPiece(PlainPiece):
    '''Inherits from the PlainPiece class and overrides some methods.

    Overrides the valid_moves- and the valid_jump_moves-methods to allow pieces to move backwards.
    Also overrides the move_piece-method to instead remove and add positions to the king_pieces_dictionary.
    '''

    def valid_moves(self):
        if self.check_if_empty_square(self.x_pos + 1, self.y_pos + 1):
            if self.x_pos + 1 < PlainPiece.board_size_list[0] and self.y_pos + 1 < PlainPiece.board_size_list[0]:
                self.valid_moves_list.append([self.x_pos + 1, self.y_pos + 1])

        if self.check_if_empty_square(self.x_pos - 1, self.y_pos + 1):
            if self.x_pos - 1 >= 0 and self.y_pos + 1 < PlainPiece.board_size_list[0]:
                self.valid_moves_list.append([self.x_pos - 1, self.y_pos + 1])

        if self.check_if_empty_square(self.x_pos + 1, self.y_pos - 1):
            if self.x_pos + 1 < PlainPiece.board_size_list[0] and self.y_pos - 1 >= 0:
                self.valid_moves_list.append([self.x_pos + 1, self.y_pos - 1])

        if self.check_if_empty_square(self.x_pos - 1, self.y_pos - 1):
            if self.x_pos - 1 >= 0 and self.y_pos - 1 >= 0:
                self.valid_moves_list.append([self.x_pos - 1, self.y_pos - 1])

        return self.valid_moves_list

    def valid_jump_moves(self):
        if self.x_pos + 2 < PlainPiece.board_size_list[0] and self.y_pos + 2 < PlainPiece.board_size_list[0]:
            if self.check_if_empty_square(self.x_pos + 2, self.y_pos + 2):
                if self.check_if_opponent_on_square(self.x_pos + 1, self.y_pos + 1):
                    self.valid_jump_moves_list.append([self.x_pos + 2, self.y_pos + 2])

        if self.x_pos - 2 >= 0 and self.y_pos + 2 < PlainPiece.board_size_list[0]:
            if self.check_if_empty_square(self.x_pos - 2, self.y_pos + 2):
                if self.check_if_opponent_on_square(self.x_pos - 1, self.y_pos + 1):
                    self.valid_jump_moves_list.append([self.x_pos - 2, self.y_pos + 2])

        if self.x_pos + 2 < PlainPiece.board_size_list[0] and self.y_pos - 2 >= 0:
            if self.check_if_empty_square(self.x_pos + 2, self.y_pos - 2):
                if self.check_if_opponent_on_square(self.x_pos + 1, self.y_pos - 1):
                    self.valid_jump_moves_list.append([self.x_pos + 2, self.y_pos - 2])

        if self.x_pos - 2 >= 0 and self.y_pos - 2 >= 0:
            if self.check_if_empty_square(self.x_pos - 2, self.y_pos - 2):
                if self.check_if_opponent_on_square(self.x_pos - 1, self.y_pos - 1):
                    self.valid_jump_moves_list.append([self.x_pos - 2, self.y_pos - 2])

        return self.valid_jump_moves_list

    def move_piece(self, new_x, new_y):
        if [self.x_pos, self.y_pos] in PlainPiece.king_pieces_dict[self.player]:
            if [new_x, new_y] in self.valid_moves():
                if not check_jump_moves(self.player):
                    PlainPiece.king_pieces_dict[self.player].append([new_x, new_y])
                    PlainPiece.king_pieces_dict[self.player].remove([self.x_pos, self.y_pos])
                    PlainPiece.AI_check_moves_dict[self.player].clear()
                    PlainPiece.AI_check_jump_moves_dict[self.player].clear()
                else:
                    raise EnvironmentError("You must take a piece if you can!")

            elif [new_x, new_y] in self.valid_jump_moves():
                self.check_which_piece_captured(new_x, new_y)
                PlainPiece.king_pieces_dict[self.player].append([new_x, new_y])
                PlainPiece.king_pieces_dict[self.player].remove([self.x_pos, self.y_pos])
                PlainPiece.AI_check_moves_dict[self.player].clear()
                PlainPiece.AI_check_jump_moves_dict[self.player].clear()
                if KingPiece(new_x, new_y, self.player).valid_jump_moves():
                    PlainPiece.jump_again_list.clear()
                    PlainPiece.jump_again_list.append([new_x, new_y])
                else:
                    PlainPiece.jump_again_list.clear()
            else:
                raise ValueError("That is not a valid move!")
        else:
            raise TypeError("You must select a piece of your own!")
        return


def clear_dictionaries():
    '''Clears all the dictionaries.

    :return: (nothing)
    '''

    PlainPiece.jump_again_list.clear()
    PlainPiece.AI_check_moves_dict[1].clear()
    PlainPiece.AI_check_moves_dict[2].clear()
    PlainPiece.AI_check_jump_moves_dict[1].clear()
    PlainPiece.AI_check_jump_moves_dict[2].clear()
    PlainPiece.pieces_dict[1].clear()
    PlainPiece.pieces_dict[2].clear()
    PlainPiece.king_pieces_dict[1].clear()
    PlainPiece.king_pieces_dict[2].clear()
    return


def get_int_input(prompt_string):
    '''Used to get an int form the user, asks again if input is not convertible to an integer.

    :param prompt_string: A string explaining what to input
    :return: The int that was asked for
    '''

    while True:

        try:
            answer = int(input(prompt_string + '\n'))

        except ValueError:
            print('You must enter a number!')

        else:
            break

    return answer


def print_start_board(empty_rows):
    '''Prints the starting board and adds every piece to the pieces dictionary.

    :param empty_rows: Used to calculate which rows that should be empty
    :return:
    '''

    player1 = " A "
    player2 = " B "

    start_board = [[" - "] * PlainPiece.board_size_list[0] for _ in range(PlainPiece.board_size_list[0])]
    for row in range(empty_rows):
        for column in range(PlainPiece.board_size_list[0]):
            if row % 2 == 0:
                if column % 2 != 0:
                    start_board[row][column] = player2
                    new_piece = [column, row]
                    PlainPiece.pieces_dict[2].append(new_piece)

            elif row % 2 != 0:

                if column % 2 == 0:
                    start_board[row][column] = player2
                    new_piece = [column, row]
                    PlainPiece.pieces_dict[2].append(new_piece)

    for row in range(PlainPiece.board_size_list[0] - empty_rows, PlainPiece.board_size_list[0]):
        for column in range(PlainPiece.board_size_list[0]):
            if row % 2 == 0:
                if column % 2 != 0:
                    start_board[row][column] = player1
                    new_piece = [column, row]
                    PlainPiece.pieces_dict[1].append(new_piece)
            elif row % 2 != 0:

                if column % 2 == 0:
                    start_board[row][column] = player1
                    new_piece = [column, row]
                    PlainPiece.pieces_dict[1].append(new_piece)

    for row in start_board:
        startBoard = "".join(row)
        print(startBoard)
    print()

    return


# Uses the coordinates in the dictionaries to print the current board
def print_current_board():
    '''Prints the current board using the dictionaries with all the positions.

    :return: (nothing)
    '''

    player1 = " A "
    player2 = " B "

    board = [[" - "] * PlainPiece.board_size_list[0] for _ in range(PlainPiece.board_size_list[0])]
    for player in PlainPiece.pieces_dict:
        for coordinate in PlainPiece.pieces_dict[player]:
            if player == 1:
                board[coordinate[1]][coordinate[0]] = player1
            elif player == 2:
                board[coordinate[1]][coordinate[0]] = player2
    for players in PlainPiece.king_pieces_dict:
        for coord in PlainPiece.king_pieces_dict[players]:
            if players == 1:
                board[coord[1]][coord[0]] = player1
            elif players == 2:
                board[coord[1]][coord[0]] = player2

    for _ in board:
        board = "".join(_)
        print(board)
    print()

    return


def add_high_score(name, board_size, start, end):
    '''Adds information to the  high score file about the winning player.

    :param name: The name of the winning player
    :param board_size: The size of the board
    :param start: The time at which the game started
    :param end: The time at which the game ended
    :return:
    '''
    
    if board_size == 8:
        size = "8x8"
    else:
        size = "10x10"
    if name != "Player 1" and name != "Player 2":
        duration = str(int(end-start))
        high_score_list = [name.replace(' ', ''), size, duration]
        with open("Highscore.txt", 'a') as f:
            f.write(high_score_list[0] + ' ' + high_score_list[1] + ' ' + high_score_list[2] + "\n")
    return


def view_high_score():
    '''Reads from the high score file and prints the current high score list.

    :return: (nohting)
    '''

    time_list_8 = []
    name_list_8 = []
    time_list_10 = []
    name_list_10 = []

    with open('Highscore.txt', 'r') as f:
        score_list = [line.split(' ') for line in f.read().splitlines()]
        for lists in score_list:
            if lists[1] == "8x8":
                time_list_8.append(lists[2])
                name_list_8.append([lists[0], lists[1]])
            elif lists[1] == "10x10":
                time_list_10.append(lists[2])
                name_list_10.append([lists[0], lists[1]])

    time_list_8.sort()
    time_list_8 = time_list_8[:10]
    time_list_10.sort()
    time_list_10 = time_list_10[:10]

    print("\033[4m\033[1m8x8\033[0m")
    for times in range(len(time_list_8)):
        m, s = divmod(int(time_list_8[times]), 60)
        if name_list_8[times][1] == "8x8":
            print("%d min %02d s  " % (m, s) + " " + name_list_8[times][0])

    print("\033[4m\033[1m10x10\033[0m")
    for times in range(len(time_list_10)):
        m, s = divmod(int(time_list_10[times]), 60)
        if name_list_10[times][1] == "10x10":
            print("%d min %02d s  " % (m, s) + " " + name_list_10[times][0])
    return


def check_jump_moves(player):
    '''Used to check if a player can take a piece.

    :param player: Which player it is
    :return: Boolean variable. True if a jump move is possible and False if a jump move is not possible
    '''

    # Stores all available jump moves that each player can make
    check_jump_moves_dict = {1: [], 2: []}

    for coord_pair in PlainPiece.pieces_dict[player]:
        jump_piece = PlainPiece(coord_pair[0], coord_pair[1], player)
        if jump_piece.valid_jump_moves():
            check_jump_moves_dict[player].append(PlainPiece(coord_pair[0], coord_pair[1], player).valid_jump_moves())
            PlainPiece.AI_check_jump_moves_dict[player].append([coord_pair[0], coord_pair[1]])
    for coord_pair in PlainPiece.king_pieces_dict[player]:
        if KingPiece(coord_pair[0], coord_pair[1], player).valid_jump_moves():
            check_jump_moves_dict[player].append(KingPiece(coord_pair[0], coord_pair[1], player).valid_jump_moves())
            PlainPiece.AI_check_jump_moves_dict[player].append([coord_pair[0], coord_pair[1]])
    if not check_jump_moves_dict[player]:
        return False
    else:
        return True


def no_valid_moves(player):
    '''Used to check if a player can make a valid move.

    :param player: Which player it is
    :return: Boolean variable. True if no valid move is possible, False if there is a possible move
    '''

    # Stores all available moves that each player can make
    no_valid_moves_dict = {1: [], 2: []}

    for coordPair in PlainPiece.pieces_dict[player]:
        if PlainPiece(coordPair[0], coordPair[1], player).valid_moves():
            no_valid_moves_dict[player].append(coordPair)
            PlainPiece.AI_check_moves_dict[player].append(coordPair)
    for coordPair in PlainPiece.pieces_dict[player]:
        if PlainPiece(coordPair[0], coordPair[1], player).valid_jump_moves():
            no_valid_moves_dict[player].append(coordPair)
            PlainPiece.AI_check_moves_dict[player].append(coordPair)
    for coordPair in PlainPiece.king_pieces_dict[player]:
        if KingPiece(coordPair[0], coordPair[1], player).valid_moves():
            no_valid_moves_dict[player].append(coordPair)
            PlainPiece.AI_check_moves_dict[player].append(coordPair)
    for coordPair in PlainPiece.king_pieces_dict[player]:
        if KingPiece(coordPair[0], coordPair[1], player).valid_jump_moves():
            no_valid_moves_dict[player].append(coordPair)
            PlainPiece.AI_check_moves_dict[player].append(coordPair)
    if not no_valid_moves_dict[player]:
        return True
    else:
        return False


def move_piece_on_board(player):
    '''Asks the player which move they want to make and moves the piece.

    Asks for the coordinates the piece's current position and the coordinates where the player wants to move it.
    If the players own piece is not selected or if the move is invalid, it will ask again.
    :param player: The player whose turn it is
    :return: (nothing)
    '''

    while True:
        print("It is player " + str(player) + ":s turn to move")
        # If a piece can make another jump move the user will be asked to only enter the new coordinates for that piece
        if PlainPiece.jump_again_list:
            past_x = PlainPiece.jump_again_list[0][0]
            past_y = PlainPiece.jump_again_list[0][1]
            PlainPiece.jump_again_list.clear()
        else:
            past_x = get_int_input("What's the current x-coordinate of the piece you want to move?")
            past_y = get_int_input("What's the current y-coordinate of the piece you want to move?")
        new_x = get_int_input("Enter the new x-coordinate for your piece")
        new_y = get_int_input("Enter the new y-coordinate for your piece")

        if [past_x, past_y] in PlainPiece.king_pieces_dict[player]:
            try:
                piece = KingPiece(past_x, past_y, player)
                if piece.move_piece(new_x, new_y):
                    return True
            except EnvironmentError as error:
                print(error)
            except TypeError as error:
                print(error)
            except ValueError as error:
                print(error)
            else:
                return False

        if [past_x, past_y] in PlainPiece.pieces_dict[player]:
            try:
                piece = PlainPiece(past_x, past_y, player)
                if piece.move_piece(new_x, new_y):
                    return True
            except EnvironmentError as error:
                print(error)
            except TypeError as error:
                print(error)
            except ValueError as error:
                print(error)
            else:
                return False


def AI_move_piece_on_board(player):
    '''Makes a random move for a player.

    Used to move a piece for the AI.
    :param player: The player whose turn it is
    :return:
    '''

    if PlainPiece.jump_again_list:
        if [PlainPiece.jump_again_list[0][0], PlainPiece.jump_again_list[0][1]] in PlainPiece.pieces_dict[player]:
            AI_piece = PlainPiece(PlainPiece.jump_again_list[0][0], PlainPiece.jump_again_list[0][1], player)
            AI_new_pos = random.choice(AI_piece.valid_jump_moves())
            AI_piece.move_piece(AI_new_pos[0], AI_new_pos[1])
        elif [PlainPiece.jump_again_list[0][0], PlainPiece.jump_again_list[0][1]] \
                in PlainPiece.king_pieces_dict[player]:
            AI_piece = KingPiece(PlainPiece.jump_again_list[0][0], PlainPiece.jump_again_list[0][1], player)
            AI_new_pos = random.choice(AI_piece.valid_jump_moves())
            AI_piece.move_piece(AI_new_pos[0], AI_new_pos[1])
    elif check_jump_moves(player):
        # Selects a random legal jump move to make
        AI_past_pos = random.choice(PlainPiece.AI_check_jump_moves_dict[player])
        if AI_past_pos in PlainPiece.pieces_dict[player]:
            AI_piece = PlainPiece(AI_past_pos[0], AI_past_pos[1], player)
            AI_new_pos = random.choice(AI_piece.valid_jump_moves())
            AI_piece.move_piece(AI_new_pos[0], AI_new_pos[1])
        elif AI_past_pos in PlainPiece.king_pieces_dict[player]:
            AI_piece = KingPiece(AI_past_pos[0], AI_past_pos[1], player)
            AI_new_pos = random.choice(AI_piece.valid_jump_moves())
            AI_piece.move_piece(AI_new_pos[0], AI_new_pos[1])
        return True
    elif not no_valid_moves(player):
        # Selects a random legal regular move to make
        AI_past_pos = random.choice(PlainPiece.AI_check_moves_dict[player])
        if AI_past_pos in PlainPiece.pieces_dict[player]:
            AI_piece = PlainPiece(AI_past_pos[0], AI_past_pos[1], player)
            AI_new_pos = random.choice(AI_piece.valid_moves())
            AI_piece.move_piece(AI_new_pos[0], AI_new_pos[1])
        elif AI_past_pos in PlainPiece.king_pieces_dict[player]:
            AI_piece = KingPiece(AI_past_pos[0], AI_past_pos[1], player)
            AI_new_pos = random.choice(AI_piece.valid_moves())
            AI_piece.move_piece(AI_new_pos[0], AI_new_pos[1])
            PlainPiece.jump_again_list.clear()
        return True
    else:
        return False


def game(player, AI = False):
    '''Starts the game using the different functions and alternating between the players' turn until one wins.

    :return: (nothing)
    '''

    empty_rows = 3

    print("---------Welcome to checkers---------\n")

    while True:
        board_size = get_int_input("Which board size do you want? 8 or 10?")
        if board_size == 8:
            break
        elif board_size == 10:
            empty_rows = 4
            PlainPiece.board_size_list[0] = 10
            break
        else:
            print("That board size is not available")

    if not AI:
        player_1_name = input("What's the name of player 1?")
        player_2_name = input("What's the name of player 2?")
        print_start_board(empty_rows)
        start_time = time()

        while True:
            if no_valid_moves(1):
                print("Congratulations! Player 2 wins!!")
                end_time = time()
                add_high_score(player_2_name, board_size, start_time, end_time)
                break
            check_jump_moves(1)
            move_piece_on_board(1)
            print_current_board()
            while PlainPiece.jump_again_list:
                check_jump_moves(1)
                move_piece_on_board(1)
                print_current_board()
            if no_valid_moves(2):
                print("Congratulations! Player 1 wins!!")
                end_time = time()
                add_high_score(player_1_name, board_size, start_time, end_time)
                break
            check_jump_moves(2)
            move_piece_on_board(2)
            print_current_board()
            while PlainPiece.jump_again_list:
                check_jump_moves(2)
                print(PlainPiece.jump_again_list)
                move_piece_on_board(2)
                print_current_board()

    elif AI and player == 1:
        player_1_name = input("What's the name of player 1?")
        print_start_board(empty_rows)
        start_time = time()

        while True:
            if no_valid_moves(1):
                print("AI wins!")
                break
            check_jump_moves(1)
            move_piece_on_board(1)
            print_current_board()
            while PlainPiece.jump_again_list:
                check_jump_moves(1)
                move_piece_on_board(1)
                print_current_board()
            if no_valid_moves(2):
                print("Congratulations! Player 1 wins!!")
                end_time = time()
                add_high_score(player_1_name, board_size, start_time, end_time)
                break
            AI_move_piece_on_board(2)
            print_current_board()
            while PlainPiece.jump_again_list:
                AI_move_piece_on_board(2)
                print_current_board()

    elif AI and player == 2:
        player_2_name = input("What's the name of player 2?")
        print_start_board(empty_rows)
        start_time = time()

        while True:
            if no_valid_moves(1):
                print("Congratulations! Player 1 wins!!")
                end_time = time()
                add_high_score(player_2_name, board_size, start_time, end_time)
                break
            AI_move_piece_on_board(1)
            print_current_board()
            while PlainPiece.jump_again_list:
                AI_move_piece_on_board(1)
                print_current_board()
            if no_valid_moves(2):
                print("AI wins!")
                break
            check_jump_moves(2)
            move_piece_on_board(2)
            print_current_board()
            while PlainPiece.jump_again_list:
                check_jump_moves(2)
                move_piece_on_board(2)
                print_current_board()

    return


if __name__ == "__main__":
    game(1)
