"""
Tic tac toe game implemented in Python 3.x
"""

import sys



class Game:

    def __init__(self, n, player1, player2):
        self.row = n
        self.column = n
        self.total_squares = self.row * self.column
        self.player1 = player1
        self.player2 = player2

        self.ICONS = {
            self.player1: 'X',
            self.player2: 'O'
        }

        self.player1_turn = True
        self.current_player = self.player1

        self.state = self._new_game()
        self.winner = None
        self.display()

    # Core
    # -------------------------------------------------------------------------

    def get_current_player(self):
        if self.player1_turn:
            self.current_player = self.player1
        else:
            self.current_player = self.player2
        return self.current_player

    def get_icon(self):
        """Return player icon"""
        return self.ICONS[self.current_player]


    def _new_game(self):
        """Starts new game"""
        state = []
        row = []

        for i in range(self.total_squares):
            row.append(str(i + 1))
            if len(row) == self.column:
                state.append(row)
                row = []

        return state

    def _get_row_column(self, square):
        """Get the row and column index based on square value"""
        for i, row in enumerate(self.state):
            if square in row:
                return i, row.index(square)

    def _update_state(self, row, column):
        """Update the game state"""
        self.state[row][column] = self.get_icon()

    def _get_winning_combinations(self, square):
        """Get possible winning combinations of square values based on a given
        square value"""
        icon = self.get_icon()

        # Case 1: Horizontal
        for row in self.state:
            for i, square in enumerate(row):
                try:
                    if (square == icon and\
                        row[i + 1] == icon and\
                        row[i + 2] == icon):
                        self.winner = self.current_player
                        break
                except IndexError:
                    pass

        # Case 2: Vertical
        for i, row in enumerate(self.state):
            for j, square in enumerate(row):
                try:
                    if (square == icon and\
                        self.state[i + 1][j] == icon and\
                        self.state[i + 2][j] == icon):
                        self.winner = self.current_player
                        break
                except IndexError:
                    pass

        # Case 3: Diagonal - bottom right direction
        for i, row in enumerate(self.state):
            for j, square in enumerate(row):
                try:
                    if (square == icon and\
                        self.state[i + 1][j + 1] == icon and\
                        self.state[i + 2][j + 2] == icon):
                        self.winner = self.current_player
                        break
                except IndexError:
                    pass

        # Case 4: Diagonal - bottom left direction
        for i, row in enumerate(self.state):
            for j, square in enumerate(row):
                try:
                    if (square == icon and\
                        self.state[i + 1][j - 1] == icon and\
                        self.state[i + 2][j - 2] == icon):
                        self.winner = self.current_player
                        break
                except IndexError:
                    pass

        # Case 5: Diagonal - top left direction
        for i, row in enumerate(self.state):
            for j, square in enumerate(row):
                try:
                    if (square == icon and\
                        self.state[i - 1][j - 1] == icon and\
                        self.state[i - 2][j - 2] == icon):
                        self.winner = self.current_player
                        break
                except IndexError:
                    pass

        # Case 6: Diagonal - top right direction
        for i, row in enumerate(self.state):
            for j, square in enumerate(row):
                try:
                    if (square == icon and\
                        self.state[i - 1][j + 1] == icon and\
                        self.state[i - 2][j + 2] == icon):
                        self.winner = self.current_player
                        break
                except IndexError:
                    pass

    def _next_player(self):
        self.player1_turn = not self.player1_turn

    def _check_winner(self, square):
        """Checks for winner"""
        self._get_winning_combinations(square)

    # Aesthetics
    # -------------------------------------------------------------------------
    def _create_new_line(self):
        """Creates a new line"""
        each_digit = "------"
        return (each_digit * self.column) + ("-" * (self.column - 1))

    def display(self):
        """Displays current state"""
        for i, row in enumerate(self.state):
            for j, square in enumerate(row):
                if len(str(square)) > 1:
                    row[j] = '  {}  '.format(square)
                else:
                    row[j] = '  {}   '.format(square)
            print("|".join(row))
            if not i == (len(self.state) - 1):
                print(self._create_new_line())
        
        # clean up
        for row in self.state:
            for i, square in enumerate(row):
                row[i] = square.strip()

    # Player action
    # -------------------------------------------------------------------------
    def play(self, square):
        square = int(square)
        if square > self.total_squares or square < 1:
            square = input("Invalid square, please choose a valid square: ")
            return self.play(square)

        if square == self.ICONS[self.player1]\
        or square == self.ICONS[self.player2]:
            square = input(
                "Square already taken, please choose an available square: "
                )
            return self.play(square)

        row, column = self._get_row_column(str(square))

        self._update_state(row, column)
        self.display()
        self._check_winner(str(square))
        self._next_player()


# Game runner
# -----------------------------------------------------------------------------
def get_players():
    player1 = input("Enter Player 1's name: ")
    player2 = input("Enter Player 2's name: ")
    return player1, player2

def play_game():
    # Get player IDs
    player1, player2 = get_players()

    # Get board size
    valid_board_size = False

    while not valid_board_size:
        board_size = int(input("Set `n` where `n x n` is the board size (min 3): "))
        if board_size >= 3:
            valid_board_size = True

    # Start game
    game = Game(board_size, player1, player2)

    while not game.winner:
        square = input(
                    "{}'s turn (icon: '{}'), choose your preferred square: "\
                    .format(
                        game.get_current_player(),
                        game.get_icon()
                    )
                 )
        game.play(square)

    print("The winner is {}.".format(game.winner))
    print("---------------------------------------")
    again = input("Would you like to play again? (y/n): ").lower()

    if again == 'y':
        play_game()
    else:
        sys.exit()


# Run game
# -----------------------------------------------------------------------------
play_game()