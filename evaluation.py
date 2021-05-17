""""
Will contain multiple different move-evaluation algorithms 
"""
import chess
import constants
import random
import game


class BaseEngine:
    
    def __init__(self, board, made_moves, user):
        self.board = board
        self.made_moves = made_moves
        self.user = user

    def is_opening(self):
        """
        Check if the game is in the opening phase
        """
        if self.board.fullmove_number <= 5:
            return True
        return False

    def get_opening_move(self):

        self.sicilian = [['e2e4', 'g1f3', 'd2d4', 'f3d4'], ['c7c5', 'd7d6', 'c5d4', 'g8f6']]
        self.q_gambit = [['d2d4', 'c2c4', 'b1c3', 'g1f3'], ['d7d5', 'e7e6', 'g8f6', 'c7c6']]

        # Engine playing black
        if self.user == chess.WHITE:
            
            # open sicilian
            try:
                if self.made_moves[0]=='e2e4':
                    try:
                        if self.made_moves[2] == 'g1f3':
                            pass
                            try:
                                if self.made_moves[4] == 'd2d4':
                                    pass
                                    try:
                                        if self.made_moves[6] == 'f3d4':
                                            return 'g8f6'
                                    except:
                                        return str('c5d4')
                            except:
                                return str('d7d6')
                    except:
                        return str('c7c5')
            except:
                return None

            # queens gambit declined
            try:
                if self.made_moves[0]=='d2d4':
                    try:
                        if self.made_moves[2] == 'c2c4':
                            pass
                            try:
                                if self.made_moves[4] == 'b1c3':
                                    pass
                                    try:
                                        if self.made_moves[6] == 'g1f3':
                                            return 'c7c6'
                                    except:
                                        return str('g8f6')
                            except:
                                return str('e7e6')
                    except:
                        return str('d7d5')
            except:
                return None


        # Engine playing white
        if self.user == chess.BLACK:

            if self.made_moves == []:
                return 'e2e4'

            # open sicilian
            try:
                if self.made_moves[1]=='c7c5':
                    try:
                        if self.made_moves[3] == 'd7d6':
                            pass
                            try:
                                if self.made_moves[5] == 'c5d4':
                                    pass
                                    try:
                                        if self.made_moves[7] == 'g8f6':
                                            return 'b1c3'
                                    except:
                                        return str('f3d4')
                            except:
                                return str('d2d4')
                    except:
                        return str('g1f3')
            except:
                return None


    def make_opening_move(self):
        self.move = self.get_opening_move()
        for legal_move in self.board.legal_moves:
            if self.move == str(legal_move):
                return legal_move



class RandomEval(BaseEngine):
    """
    Engine class that does no board evalatuon but produces a random move.

    Functions:
    Init intitiates the class with the current board from game.py
    make_move(): loops through legal moves and returns a random legal move
    """

    def __init__(self, board, made_moves, user):
        super().__init__(board, made_moves, user)
    

    def make_move(self):
        self.moves = self.board.legal_moves

        self.moves = []
        for move in self.board.legal_moves:
            self.moves.append(str(move))
        self.random_move = self.moves[random.randrange(0, len(self.moves))]

        return self.random_move



class SimpleEval(BaseEngine):
    """
    Engine Class performing a simple evaluation inspired by Michniewski's simple evaluation;
    https://www.chessprogramming.org/Simplified_Evaluation_Function


    Functions:
    is_end_game() : takes no arguments and determines end-game status by simple piece evaluation
    evaluate_piece() : gets the current value of a given piece estimated from its intrinsic value added by the piece-square table value.
    is_capture() : checks whether a move is a capture
    evaluate_capture() : evaluates whether a trade is favorable
    is_attacked() : checks whether a given move will place the piece under attack
    is_defended() : check whether a given move will place the piece on a defended square
    evaluate_board() : makes an evaluation of the board by calculating the values from evaluate_piece() for all pieces on the board.
    evaluate_move() : makes use of above-stated evaluation functions to find the best move in the current position.

    """


    def __init__(self, board, made_moves, user):
        super().__init__(board, made_moves, user)
    

    def is_end_game(self):
        queens = 0
        minors = 0

        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if not piece:
                continue
            if piece.piece_type == chess.QUEEN:
                queens += 1
            if (piece.piece_type == chess.BISHOP or piece.piece_type == chess.KNIGHT):
                minors += 1
        
        if queens == 0 or (queens == 2 and minors <= 1):
            return True


    def evaluate_piece(self, piece, loc):

        type = piece.piece_type
        
        if piece.color == chess.WHITE:
            if type == chess.PAWN:
                return constants.piece_value[1] + constants.white_pawn[loc]
            if type == chess.KNIGHT:
                return constants.piece_value[2] + constants.knight[loc]
            if type == chess.BISHOP:
                return constants.piece_value[3] + constants.white_bishop[loc]
            if type == chess.ROOK:
                return constants.piece_value[4] + constants.white_rook[loc]
            if type == chess.QUEEN:
                return constants.piece_value[5] + constants.queen[loc]
            if type == chess.KING:
                if self.is_end_game():
                    return constants.piece_value[6] + constants.white_king_end
                else:
                    return constants.piece_value[6] + constants.white_king_mid

        elif piece.color == chess.BLACK:
            if type == chess.PAWN:
                return constants.piece_value[1] + constants.black_pawn[loc]
            if type == chess.KNIGHT:
                return constants.piece_value[2] + constants.knight[loc]
            if type == chess.BISHOP:
                return constants.piece_value[3] + constants.black_bishop[loc]
            if type == chess.ROOK:
                return constants.piece_value[4] + constants.black_rook[loc]
            if type == chess.QUEEN:
                return constants.piece_value[5] + constants.queen[loc]
            if type == chess.KING:
                if self.is_end_game():
                    return constants.piece_value[6] + constants.black_king_end[loc]
                else:
                    return constants.piece_value[6] + constants.black_king_mid[loc]

    
    def is_capture(self, _sq):
        _sq = self.board.piece_at(_sq)
        if _sq is None:
            return False
        return True
    

    def evaluate_capture(self, to_sq, from_sq):
        piece_1 = self.board.piece_at(to_sq).piece_type
        piece_2 = self.board.piece_at(from_sq).piece_type

        if (constants.piece_value[piece_1] - constants.piece_value[piece_2]) >= 0:
            return True
        return False

    
    def is_attacked(self, move):
        tmp_board = self.board.copy()
        tmp_board.push(move)
        for attack in tmp_board.legal_moves:
            if attack.to_square == move.to_square:
                return True
        return False
    

    def is_defended(self, move):
        def_count = 0
        for other_move in self.board.legal_moves:
            if other_move == move:
                continue
            if other_move.to_square == move.to_square:
                if self.board.piece_at(other_move.to_square).piece_type == chess.KING:
                    continue
                def_count += 1

        return def_count


    def evaluate_board(self):
        total = 0
        for sq in chess.SQUARES:
            piece = self.board.piece_at(sq)

            if not piece:
                continue

            value = self.evaluate_piece(piece, sq)

            if piece.color == chess.WHITE:
                total += value
            elif piece.color == chess.BLACK:
                total -= value
            
            return total


    def evaluate_move(self):

        move_val = 0

        cur_best_move = None

        for move in self.board.legal_moves:

            if cur_best_move == None:
                cur_best_move = move


            loc = move.from_square
            new_loc = move.to_square
            piece = self.board.piece_at(loc)
            value = self.evaluate_piece(piece, loc)
            new_value = self.evaluate_piece(piece, new_loc)

            if new_value > value:
                if (new_value - value) > move_val:
                    cur_best_move = move

        return cur_best_move