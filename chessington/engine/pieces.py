"""
Definitions of each of the different chess pieces.
"""

from abc import ABC, abstractmethod

from chessington.engine.data import Player, Square


class Piece(ABC):
    """
    An abstract base class from which all pieces inherit.
    """

    def __init__(self, player):
        self.player = player

    @abstractmethod
    def get_available_moves(self, board):
        """
        Get all squares that the piece is allowed to move to.
        """
        pass

    def move_to(self, board, new_square):
        """
        Move this piece to the given square on the board.
        """
        current_square = board.find_piece(self)
        board.move_piece(current_square, new_square)

    def on_board(self, board, square):
        board_size = len(board.board)
        if square.row < 0 or square.row > board_size - 1:
            return False
        if square.col < 0 or square.col > board_size - 1:
            return False
        return True

    def obstructed_colour(self, board, square):
        piece = board.get_piece(square)
        if piece is None:
            return None
        else:
            return piece.player

    def obstructed_path(self, board, square):
        current_square = board.find_piece(self)
        target_square = square
        check_square = board.find_piece(self)
        row_add = 0
        col_add = 0
        if current_square.row > target_square.row:
            row_add = -1
        elif current_square.row < target_square.row:
            row_add = +1
        if current_square.col > target_square.col:
            col_add = -1
        elif current_square.col < target_square.col:
            col_add = +1
        for i in range(8):
            check_square = square.at(check_square.row + row_add, check_square.col + col_add)
            if target_square == check_square:
                return False
            if self.obstructed_colour(board, check_square) is not None:
                return True
        return True


class Pawn(Piece):
    """
    A class representing a chess pawn.
    """

    def get_available_moves(self, board):

        current = board.find_piece(self)
        row = current.row
        col = current.col
        possible_moves = []

        if self.player == Player.WHITE:
            possible_moves.append(Square.at(row + 1, col))
            if row == 1:
                possible_moves.append(Square.at(row + 2, col))

        else:
            possible_moves.append(Square.at(row - 1, col))
            if row == 6:
                possible_moves.append(Square.at(row - 2, col))

        possible_moves = list(filter(lambda p: self.on_board(board, p), possible_moves))
        possible_moves = list(filter(lambda p: self.obstructed_colour(board, p) is None, possible_moves))

        capture_moves = []

        if self.player == Player.WHITE:
            capture_moves.append(Square.at(row + 1, col + 1))
            capture_moves.append(Square.at(row + 1, col - 1))
            capture_moves = list(filter(lambda p: self.on_board(board, p), capture_moves))
            capture_moves = list(filter(lambda p: self.obstructed_colour(board, p) is Player.BLACK, capture_moves))

        else:
            capture_moves.append(Square.at(row - 1, col + 1))
            capture_moves.append(Square.at(row - 1, col - 1))
            capture_moves = list(filter(lambda p: self.on_board(board, p), capture_moves))
            capture_moves = list(filter(lambda p: self.obstructed_colour(board, p) is Player.WHITE, capture_moves))

        possible_moves.extend(capture_moves)

        possible_moves = list(filter(lambda p: self.obstructed_path(board, p) is False, possible_moves))

        return possible_moves


class Knight(Piece):
    """
    A class representing a chess knight.
    """

    def get_available_moves(self, board):
        return []


class Bishop(Piece):
    """
    A class representing a chess bishop.
    """

    def get_available_moves(self, board):
        return []


class Rook(Piece):
    """
    A class representing a chess rook.
    """

    def get_available_moves(self, board):
        return []


class Queen(Piece):
    """
    A class representing a chess queen.
    """

    def get_available_moves(self, board):
        return []


class King(Piece):
    """
    A class representing a chess king.
    """

    def get_available_moves(self, board):
        return []
