from enum import Enum, auto

# These boards will actually be pulled from the database in the final
# but for now, I'm leaving these to show the format

class _Winner(Enum):
    X = auto()
    O = auto()
    ONGOING = auto()
    TIE = auto()

class _Player(Enum):
    X = auto()
    O = auto()

class _SpaceType(Enum):
    X = auto()
    O = auto()
    EMPTY = auto()
    VOID = auto()

class Reversi:
    def __init__(self, board_state:list[list[_SpaceType]]):
        self.board_state = board_state
        self.turn = _Player.X

    @staticmethod
    def from_board_string(board_str:str, turn:_Player = _Player.X) -> 'Reversi':

        board = []
        line = []
        line_length = None

        for c in board_str:
            if c == 'x':
                line.append(_SpaceType.X)
            elif c == 'o':
                line.append(_SpaceType.O)
            elif c == '.':
                line.append(_SpaceType.EMPTY)
            elif c == '_':
                line.append(_SpaceType.VOID)
            elif c.isspace():
                board.append(line)

                if line_length is None:
                    line_length = len(line)
                elif line_length != len(line):
                    raise IndexError("Uneven line lengths")

                line = []

        if len(line) != 0:
            board.append(line)

            if line_length is None:
                line_length = len(line)
            elif line_length != len(line):
                raise IndexError("Uneven line lengths")


        game = Reversi(board)
        game.turn = turn
        return game

    def __str__(self) -> str:
        ret = ""
        for line in self.board_state:
            for square in line:
                if square == _SpaceType.X:
                    ret += "x"
                elif square == _SpaceType.O:
                    ret += "o"
                elif square == _SpaceType.EMPTY:
                    ret += "."
                elif square == _SpaceType.VOID:
                    ret += "_"
            ret += " "
        return ret

    def _copy_board_state(self, board:list[list[_SpaceType]])->list[list[_SpaceType]]:
        new_board = []
        for line in board:
            new_line = []
            for square in line:
                new_line.append(square)
            new_board.append(new_line)
        return new_board

    def _calc_play_in_dir(self, board:list[list[_SpaceType]], player_stone:_SpaceType, opponent_stone:_SpaceType, x:int, y:int, lr:int, ud:int)->tuple[list[list[_SpaceType]], int]:
        new_board_state = self._copy_board_state(board)
        num_flipped_stones = 0

        look_x = x+lr
        look_y = y+ud

        try:
            while True:
                if look_x < 0 or look_y < 0:
                    # Python allows a negative index
                    # We do not
                    raise IndexError

                look_stone = board[look_y][look_x]
                if look_stone in [_SpaceType.EMPTY, _SpaceType.VOID]:
                    # There was no player_stone at the end, so no flips happen
                    return (board, 0)
                elif look_stone == opponent_stone:
                    new_board_state[look_y][look_x] = player_stone
                    num_flipped_stones += 1
                elif look_stone == player_stone:
                    # We've reached the last stone in our journey
                    break

                look_x += lr
                look_y += ud
                
        except IndexError:
            # we went off the edge of the board
            return (board, 0)

        return (new_board_state, num_flipped_stones)

    def _calc_move(self, board:list[list[_SpaceType]], player:_Player, x:int, y:int)->tuple[list[list[_SpaceType]], int]:
        if x < 0 or y < 0 or y >= len(board) or x >= len(board[0]):
            return (board, 0)
        
        if self.board_state[y][x] != _SpaceType.EMPTY:
            return (board, 0)

        new_board_state = self._copy_board_state(board)
        num_flipped_stones = 0
        player_stone = _SpaceType.X if player == _Player.X else _SpaceType.O
        opponent_stone = _SpaceType.O if player == _Player.X else _SpaceType.X

        new_board_state[y][x] = player_stone

        new_board_state, new_flips = self._calc_play_in_dir(new_board_state, player_stone, opponent_stone, x, y, 0, 1)
        num_flipped_stones += new_flips
        new_board_state, new_flips = self._calc_play_in_dir(new_board_state, player_stone, opponent_stone, x, y, 1, 1)
        num_flipped_stones += new_flips
        new_board_state, new_flips = self._calc_play_in_dir(new_board_state, player_stone, opponent_stone, x, y, 1, 0)
        num_flipped_stones += new_flips
        new_board_state, new_flips = self._calc_play_in_dir(new_board_state, player_stone, opponent_stone, x, y, 1, -1)
        num_flipped_stones += new_flips
        new_board_state, new_flips = self._calc_play_in_dir(new_board_state, player_stone, opponent_stone, x, y, 0, -1)
        num_flipped_stones += new_flips
        new_board_state, new_flips = self._calc_play_in_dir(new_board_state, player_stone, opponent_stone, x, y, -1, -1)
        num_flipped_stones += new_flips
        new_board_state, new_flips = self._calc_play_in_dir(new_board_state, player_stone, opponent_stone, x, y, -1, 0)
        num_flipped_stones += new_flips
        new_board_state, new_flips = self._calc_play_in_dir(new_board_state, player_stone, opponent_stone, x, y, -1, 1)
        num_flipped_stones += new_flips
        
        if num_flipped_stones == 0:
            return (board, 0)

        return (new_board_state, num_flipped_stones)

    def play_move(self, x:int, y:int)->None:
        new_board_state, num_flipped_stones = self._calc_move(self.board_state, self.turn, x, y)

        if num_flipped_stones == 0:
            raise ValueError

        self.board_state = new_board_state
        self.turn = _Player.X if self.turn == _Player.O else _Player.O

    def get_valid_moves(self)->list[tuple[int,int]]:
        valid = []
        for y in range(len(self.board_state)):
            for x in range(len(self.board_state[0])):
                _, num_flipped_stones = self._calc_move(self.board_state, self.turn, x, y)
                if num_flipped_stones != 0:
                    valid.append((x,y))
        return valid

    def get_winner(self)->_Winner:
        if len(self.get_valid_moves()) != 0:
            return _Winner.ONGOING
        
        x_count = 0
        o_count = 0

        for line in self.board_state:
            for square in line:
                if square == _SpaceType.X:
                    x_count += 1
                elif square == _SpaceType.O:
                    o_count += 1
        if x_count > o_count:
            return _Winner.X
        if o_count > x_count:
            return _Winner.O
        return _Winner.TIE
