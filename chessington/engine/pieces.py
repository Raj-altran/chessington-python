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
        self.turn_first_moved = 0

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

    def en_passant_possible(self, board, square):
        if not isinstance(self, Pawn):
            return False
        current_square = board.find_piece(self)
        target_square = square
        piece_square = Square.at(current_square.row, target_square.col)
        piece = board.get_piece(piece_square)
        if isinstance(piece, Pawn):
            if piece.turn_first_moved == board.turn - 1:
                if piece.player != self.player:
                    return True
        return False


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

        possible_moves = list(filter(lambda s: self.on_board(board, s), possible_moves))
        possible_moves = list(filter(lambda s: self.obstructed_colour(board, s) is None, possible_moves))

        capture_moves = []

        if self.player == Player.WHITE:
            capture_moves.append(Square.at(row + 1, col + 1))
            capture_moves.append(Square.at(row + 1, col - 1))
            capture_moves = list(filter(lambda s: self.on_board(board, s), capture_moves))
            capture_moves = list(
                filter(lambda s: self.obstructed_colour(board, s) is Player.BLACK or self.en_passant_possible(board, s),
                       capture_moves))
        else:
            capture_moves.append(Square.at(row - 1, col + 1))
            capture_moves.append(Square.at(row - 1, col - 1))
            capture_moves = list(filter(lambda s: self.on_board(board, s), capture_moves))
            capture_moves = list(
                filter(lambda s: self.obstructed_colour(board, s) is Player.WHITE or self.en_passant_possible(board, s),
                       capture_moves))

        possible_moves.extend(capture_moves)

        possible_moves = list(filter(lambda s: self.obstructed_path(board, s) is False, possible_moves))

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

        current = board.find_piece(self)
        row = current.row
        col = current.col
        possible_moves = []

        for i in range(8):
            possible_moves.append(Square.at(i, col))

        for i in range(8):
            possible_moves.append(Square.at(row, i))

        possible_moves = list(filter(lambda s: self.on_board(board, s), possible_moves))
        possible_moves = list(filter(lambda s: self.obstructed_colour(board, s) is not self.player, possible_moves))
        possible_moves = list(filter(lambda s: not self.obstructed_path(board, s), possible_moves))

        return possible_moves


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
