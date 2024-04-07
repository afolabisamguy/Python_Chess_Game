import copy

from const import *
from square import Square
from piece import *
from move import Move


class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        # console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # pawn promotion
        if isinstance(piece, Pawn):
            self.check_promotion(piece, final)

        if isinstance(piece, King):
            if self.castling(initial, final):
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])

        # move
        piece.moved = True

        # clear valid move
        piece.clear_moves()

        # set last move
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # pawn
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishop

        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks

        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # queens

        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # king

        self.squares[row_other][4] = Square(row_other, 4, King(color))

    def calc_moves(self, piece, row, col, bool=True):
        """
        Calculates all the possible moves of a specific piece on the board
        :param piece:
        :param row:
        :param col:
        :return:
        """

        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row - 2, col + 1),
                (row - 1, col + 2),
                (row + 1, col + 2),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row + 1, col - 2),
                (row - 1, col - 2),
                (row - 2, col - 1),
            ]

            for possible_moves in possible_moves:
                possible_moves_row, possible_moves_col = possible_moves
                if Square.in_range(possible_moves_row, possible_moves_col):
                    if self.squares[possible_moves_row][possible_moves_col].isempty_or_rival(piece.color):
                        # create square of a new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_moves_row][possible_moves_col].piece
                        final = Square(possible_moves_row, possible_moves_col, final_piece)
                        # create a new move
                        move = Move(initial, final)

                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                            else:
                                break
                        else:
                            piece.add_move(move)

        def pawn_moves():
            # steps
            steps = 1 if piece.moved else 2

            # vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for move_row in range(start, end, piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].isempty():
                        # create initial and final move
                        initial = Square(row, col)
                        final = Square(move_row, col)
                        # create a new move
                        move = Move(initial, final)

                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                    # blocked
                    else:
                        break
                    # not in range
                else:
                    break

            # diagonal moves
            move_row = row + piece.dir
            move_col = [col - 1, col + 1]

            for possible_move_col in move_col:
                if Square.in_range(move_row, possible_move_col):
                    if self.squares[move_row][possible_move_col].has_rival_piece(piece.color):
                        # create initial and final move squares
                        initial = Square(row, col)
                        final_piece = self.squares[move_row][possible_move_col].piece
                        final = Square(move_row, possible_move_col, final_piece)
                        # create a new move
                        move = Move(initial, final)

                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)

                        else:
                            piece.add_move(move)

        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row_incr + row
                possible_move_col = col_incr + col

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):

                        # create squares of the possible new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)

                        move = Move(initial, final)
                        # empty
                        if self.squares[possible_move_row][possible_move_col].isempty():

                            # check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)

                            else:
                                piece.add_move(move)

                        # has enemy piece
                        elif self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                            # check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    # append new move
                                    piece.add_move(move)

                            else:
                                piece.add_move(move)
                            break
                        # has team piece
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break

                    # not in range
                    else:
                        break
                    # incrementing incrs
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            adjs = [
                (row - 1, col + 0),  # up
                (row - 1, col + 1),  # up-right
                (row + 0, col + 1),  # right
                (row + 1, col - 1),  # down right
                (row + 1, col + 1),
                (row + 1, col + 0),
                (row + 0, col - 1),
                (row - 1, col - 1),
            ]

            # normal moves
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)

                        move = Move(initial, final)

                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                            else:
                                break
                        else:
                            piece.add_move(move)

            # castling moves
            if not piece.moved:
                # queenside castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            if self.squares[row][
                                c].has_pieces():  # castling not possible cause there are pieces in between
                                break

                            if c == 3:
                                # adds left rook to king
                                piece.left_rook = left_rook
                                # rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)

                                # check potential checks
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        left_rook.add_move(moveR)
                                        # append new move
                                        piece.add_move(moveK)

                                else:
                                    left_rook.add_move(moveR)
                                    piece.add_move(moveK)

                # king castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not left_rook.moved:
                        for c in range(5, 7):
                            if self.squares[row][
                                c].has_pieces():  # castling not possible cause there are pieces in between
                                break

                            if c == 6:
                                # adds left rook to king
                                piece.right_rook = right_rook
                                # rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)

                                # king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)

                                # check potential checks
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                        right_rook.add_move(moveR)
                                        # append new move
                                        piece.add_move(moveK)

                                else:
                                    right_rook.add_move(moveR)
                                    piece.add_move(moveK)

        if isinstance(piece, Pawn):
            pawn_moves()

        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Bishop):
            straightline_moves([
                (-1, 1),  # upper right
                (-1, -1),  # upper left
                (1, 1),  # down right
                (1, -1)  # down left
            ])

        elif isinstance(piece, Rook):
            straightline_moves([
                (-1, 0),  # up
                (0, 1),  # left
                (1, 0),  # down
                (0, -1)  # right
            ])

        elif isinstance(piece, Queen):
            straightline_moves([
                (-1, 1),  # upper right
                (-1, -1),  # upper left
                (1, 1),  # down right
                (1, -1),  # down left
                (-1, 0),
                (0, 1),
                (1, 0),
                (0, -1)
            ])

        elif isinstance(piece, King):
            king_moves()

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_rival_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
        return False
