import numpy as np
import random
import copy
from abc import ABC, abstractmethod


class Cell:
    """
    Cell in peg solitaer game.
    """
    def __init__(self, value, row, column):
        self.value = value  # 0 for no peg, 1 for peg
        self.row = row
        self.column = column
        self.neighbor_pairs = []

    # getter Methods
    def get_value(self):
        """
        check this before looking for possible actions
        """
        return self.value

    def get_row(self):
        return self.row

    def get_column(self):
        return self.column

    def get_row_column(self):
        return tuple(self.row, self.column)

    def get_neighbor_pairs(self):
        return self.neighbor_pairs

    def get_possible_actions(self):
        """
        action: (row, column), (x, y)
        ( x, y) == ...
        (-1, 0) == "down"
        ( 1, 0) == "up"
        ( 0, 1) == "right"
        ( 0,-1) == "left"
        (-1,-1) == "diagonally down(left to right)"
        (+1,+1) == "diagonally up(right to left)"
        (-1,+1) == "diagonally up(left to right)"
        (+1,-1) == "diagonally down(right to left)"
        :return: return list of actions
        """
        list_of_possible_actions = []
        for element in range(len(self.neighbor_pairs)):
            pair = self.neighbor_pairs[element]
            if pair[0].get_value() != pair[1].get_value():
                for i in range(2):
                    if pair[i].get_value() == 0:
                        list_of_possible_actions.append(((self.row, self.column), (self.row - pair[i].get_row(), self.column - pair[i].get_column())))
        return list_of_possible_actions
    # setter Methods

    def add_neighbor_pair(self, pair):
        self.neighbor_pairs.append(pair)

    def set_value(self, new_value):
        self.value = new_value

    def set_row_and_column(self, new_row, new_column):
        self.row = new_row
        self.column = new_column


class Board(ABC):
    """
    virutal method: create Board as Diamond or Triangle
    """
    @abstractmethod
    def populate_board(self): pass

    @abstractmethod
    def set_neighbor_pairs(self): pass

    def set_board_array(self, new_array):
        """
        sets the board array (e.g. back to a start board)
        """
        self.board_array = new_array

    def get_board_copy(self):
        """
        :return: deep copy of array
        """
        return copy.deepcopy(self.board_array)

    def get_board_array(self):
        return self.board_array

    def get_actions(self):
        """
        :return: return list of actions by looking at all actions for each pin.
        """
        list_of_actions = []
        for i in range(self.n):
            for j in range(self.n):
                if (self.board_array[i][j] != 0) and (self.board_array[i][j].get_value() != 0):
                    if self.board_array[i][j].get_possible_actions():
                        actions_for_this_pin = self.board_array[i][j].get_possible_actions()
                        for k in range(len(actions_for_this_pin)):
                            list_of_actions.append(actions_for_this_pin[k])
        return (list_of_actions) #@ removed tuple keyword

    def in_final_state(self):
        if not self.get_actions():
            return True     # list is empty
        else:
            return False

    def get_size(self):
        return self.n

    def get_sample_action(self):
        valid_moves = self.get_actions()
        return valid_moves[random.randint(0, len(valid_moves) - 1)]

    def take_action(self, action):
        (row, column) = action[0]
        (move_offset_vertical, move_offset_horizontal) = action[1]
        self.prev_state = self.get_board_view()             # save the previous state
        self.board_array[row + move_offset_vertical][column + move_offset_horizontal].set_value(0)
        self.board_array[row - move_offset_vertical][column - move_offset_horizontal].set_value(1)
        self.board_array[row][column].set_value(0)

    def get_board_view(self):
        """
        :return: Board Information in 2d array, use this to print the board or feed this as information
        """
        visual_array = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(self.n):
                if self.board_array[i][j] != 0:
                    visual_array[i][j] = self.board_array[i][j].get_value()
        return visual_array

    def get_previous_state(self):
        return self.prev_state


class Triangular(Board):
    def __init__(self, n):
        self.n = n
        self.board_array = np.empty(shape=(self.n, self.n), dtype=object)
        self.prev_state = 0
        self.board_shape = "Triangular"

    def populate_board(self):
        tmp_list = []
        test_array = np.zeros(shape=(self.n, self.n), dtype=object)
        for i in range((self.n * (self.n + 1)) // 2):
            new_cell = Cell(1, 0, 0)
            tmp_list.append(new_cell)
        self.set_board_array(np.zeros((self.n, self.n)))
        x = np.tril_indices(self.get_size())
        test_array[x] = tmp_list
        self.board_array = test_array
        for i in range(self.n):
            for j in range(self.n):
                if self.board_array[i][j] != 0:
                    self.board_array[i][j].set_row_and_column(i, j)

    def set_neighbor_pairs(self):
        for i in range(self.n):
            for j in range(self.n):
                if (i > 0) and (i < self.n-1):
                    if (self.board_array[i+1][j] != 0) and (self.board_array[i-1][j] != 0):
                        self.board_array[i][j].add_neighbor_pair([self.board_array[i-1][j], self.board_array[i+1][j]])
                if (j > 0) and (j < self.n-1):
                    if (self.board_array[i][j+1] != 0) and (self.board_array[i][j-1] != 0):
                        self.board_array[i][j].add_neighbor_pair([self.board_array[i][j-1], self.board_array[i][j+1]])
                if (i > 0) and (j > 0) and (i < self.n-1) and (j < self.n-1):
                    if (self.board_array[i+1][j+1] != 0) and (self.board_array[i-1][j-1] != 0):
                        self.board_array[i][j].add_neighbor_pair([self.board_array[i-1][j-1], self.board_array[i+1][j+1]])


class Diamond(Board):
    def __init__(self, n):
        self.n = n
        self.board_array = np.empty(shape=(self.n, self.n), dtype=object)
        self.prev_state = 0
        self.board_shape = "Diamond"

    def populate_board(self):
        tmp_list = []
        test_array = np.zeros(shape=(self.n, self.n), dtype=object)
        for i in range(self.n ** 2):
            new_cell = Cell(1, 0, 0)
            tmp_list.append(new_cell)
        self.set_board_array(np.zeros((self.n, self.n)))
        t = tuple([np.array([x // self.n for x in range(self.n*self.n)]), np.array(self.n*[x for x in range(self.n)])]) # helps filling the array similar to triangular case
        test_array[t] = tmp_list
        self.board_array = test_array
        for i in range(self.n):
            for j in range(self.n):
                if self.board_array[i][j] != 0:         # might not need this
                    self.board_array[i][j].set_row_and_column(i, j)

    def set_neighbor_pairs(self):
        for i in range(self.n):
            for j in range(self.n):
                if (i > 0) and (i < self.n-1):
                    if (self.board_array[i+1][j] != 0) and (self.board_array[i-1][j] != 0):
                        self.board_array[i][j].add_neighbor_pair([self.board_array[i-1][j], self.board_array[i+1][j]])
                if (j > 0) and (j < self.n-1):
                    if (self.board_array[i][j+1] != 0) and (self.board_array[i][j-1] != 0):
                        self.board_array[i][j].add_neighbor_pair([self.board_array[i][j-1], self.board_array[i][j+1]])
                if (i > 0) and (j > 0) and (i < self.n-1) and (j < self.n-1):
                    if (self.board_array[i+1][j+1] != 0) and (self.board_array[i-1][j-1] != 0):
                        self.board_array[i][j].add_neighbor_pair([self.board_array[i-1][j+1], self.board_array[i+1][j-1]])


class English(Board):
    def __init__(self):
        self.n = 7
        self.board_array = np.empty(shape=(self.n, self.n), dtype=object)
        self.prev_state = 0
        self.board_shape = "English"

    def populate_board(self):
        test_array = np.zeros(shape=(self.n, self.n), dtype=object)
        tmp_list = [Cell(1, 0, 2), Cell(1, 0, 3), Cell(1, 0, 4), Cell(1, 1, 2), Cell(1, 1, 3), Cell(1, 1, 4),
                    Cell(1, 2, 0), Cell(1, 2, 1), Cell(1, 2, 2), Cell(1, 2, 3), Cell(1, 2, 4), Cell(1, 2, 5),
                    Cell(1, 2, 6), Cell(1, 3, 0), Cell(1, 3, 1), Cell(1, 3, 2), Cell(0, 3, 3), Cell(1, 3, 4),
                    Cell(1, 3, 5), Cell(1, 3, 6), Cell(1, 4, 0), Cell(1, 4, 1), Cell(1, 4, 2), Cell(1, 4, 3),
                    Cell(1, 4, 4), Cell(1, 4, 5), Cell(1, 4, 6), Cell(1, 5, 2), Cell(1, 5, 3), Cell(1, 5, 4),
                    Cell(1, 6, 2), Cell(1, 6, 3), Cell(1, 6, 4)]
        for ele in range(len(tmp_list)):
            test_array[tmp_list[ele].get_row()][tmp_list[ele].get_column()] = tmp_list[ele]
        self.board_array = test_array

    def set_neighbor_pairs(self):
        for i in range(self.n):
            for j in range(self.n):
                if (i > 0) and (i < self.n-1):
                    if (self.board_array[i+1][j] != 0) and (self.board_array[i-1][j] != 0):
                        self.board_array[i][j].add_neighbor_pair([self.board_array[i-1][j], self.board_array[i+1][j]])
                if (j > 0) and (j < self.n-1):
                    if (self.board_array[i][j+1] != 0) and (self.board_array[i][j-1] != 0):
                        self.board_array[i][j].add_neighbor_pair([self.board_array[i][j-1], self.board_array[i][j+1]])


class Penguin(Board):
    def __init__(self):
        self.n = 5
        self.board_array = np.empty(shape=(self.n, self.n), dtype=object)
        self.prev_state = 0
        self.board_shape = "Triangular"

    def populate_board(self):
        test_array = np.zeros(shape=(self.n, self.n), dtype=object)
        tmp_list = [Cell(1, 1, 0), Cell(1, 1, 1),
                    Cell(1, 2, 0), Cell(1, 2, 1), Cell(1, 2, 2),
                    Cell(1, 3, 0), Cell(1, 3, 1), Cell(1, 3, 2), Cell(1, 3, 3),
                    Cell(1, 4, 1), Cell(1, 4, 2), Cell(1, 4, 3)]
        for ele in range(len(tmp_list)):
            test_array[tmp_list[ele].get_row()][tmp_list[ele].get_column()] = tmp_list[ele]
        self.board_array = test_array

    def set_neighbor_pairs(self):
        for i in range(self.n):
            for j in range(self.n):
                if (i > 0) and (i < self.n - 1):
                    if (self.board_array[i + 1][j] != 0) and (self.board_array[i - 1][j] != 0):
                        self.board_array[i][j].add_neighbor_pair(
                            [self.board_array[i - 1][j], self.board_array[i + 1][j]])
                if (j > 0) and (j < self.n - 1):
                    if (self.board_array[i][j + 1] != 0) and (self.board_array[i][j - 1] != 0):
                        self.board_array[i][j].add_neighbor_pair(
                            [self.board_array[i][j - 1], self.board_array[i][j + 1]])
                if (i > 0) and (j > 0) and (i < self.n - 1) and (j < self.n - 1):
                    if (self.board_array[i + 1][j + 1] != 0) and (self.board_array[i - 1][j - 1] != 0):
                        self.board_array[i][j].add_neighbor_pair(
                            [self.board_array[i - 1][j - 1], self.board_array[i + 1][j + 1]])


class Square(Board):
    def __init__(self, n):
        self.n = n
        self.board_array = np.empty(shape=(self.n, self.n), dtype=object)
        self.prev_state = 0
        self.board_shape = "Square"

    def populate_board(self):
        for i in range(self.n):
            for j in range(self.n):
                self.board_array[i][j] = Cell(1, i, j)

    def set_neighbor_pairs(self):
        for i in range(self.n):
            for j in range(self.n):
                if (i > 0) and (i < self.n-1):
                    if (self.board_array[i+1][j] != 0) and (self.board_array[i-1][j] != 0):
                        self.board_array[i][j].add_neighbor_pair([self.board_array[i-1][j], self.board_array[i+1][j]])
                if (j > 0) and (j < self.n-1):
                    if (self.board_array[i][j+1] != 0) and (self.board_array[i][j-1] != 0):
                        self.board_array[i][j].add_neighbor_pair([self.board_array[i][j-1], self.board_array[i][j+1]])


class Rectangular24(Board):
    def __init__(self):
        self.n = 7
        self.board_array = np.empty(shape=(self.n, self.n), dtype=object)
        self.prev_state = 0
        self.board_shape = "English"

    def populate_board(self):
        test_array = np.zeros(shape=(self.n, self.n), dtype=object)
        tmp_list = [Cell(1, 0, 2), Cell(1, 0, 3), Cell(1, 0, 4), Cell(1, 1, 0), Cell(1, 1, 1), Cell(1, 1, 2),
                    Cell(1, 1, 3), Cell(1, 1, 4), Cell(1, 1, 5), Cell(1, 1, 6), Cell(1, 2, 0), Cell(1, 2, 1),
                    Cell(1, 2, 2), Cell(1, 2, 3), Cell(1, 2, 4), Cell(1, 2, 5), Cell(1, 2, 6), Cell(1, 3, 0),
                    Cell(1, 3, 1), Cell(1, 3, 2), Cell(1, 3, 3), Cell(1, 3, 4), Cell(1, 3, 5), Cell(1, 3, 6)]
        for ele in range(len(tmp_list)):
            test_array[tmp_list[ele].get_row()][tmp_list[ele].get_column()] = tmp_list[ele]
        self.board_array = test_array

    def set_neighbor_pairs(self):
        for i in range(self.n):
            for j in range(self.n):
                if (i > 0) and (i < self.n-1):
                    if (self.board_array[i+1][j] != 0) and (self.board_array[i-1][j] != 0):
                        self.board_array[i][j].add_neighbor_pair([self.board_array[i-1][j], self.board_array[i+1][j]])
                if (j > 0) and (j < self.n-1):
                    if (self.board_array[i][j+1] != 0) and (self.board_array[i][j-1] != 0):
                        self.board_array[i][j].add_neighbor_pair([self.board_array[i][j-1], self.board_array[i][j+1]])
