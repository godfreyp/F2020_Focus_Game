# Author: Patrick Godfrey
# Date: 11/25/2020
# Description: A class named FocusGame for playing an abstract board game called Focus/Domination. It is a
# two player game played on a 6x6 board. Players will input their name and colors. Coordinates are input
# via tuples. The first player to six points captured is the winner.

class FocusGame:
    """
    A class that contains the board game Focus
    """
    def __init__(self, player1, player2,):
        """Initializes the FocusGame data"""
        self._p1 = list(player1)[0]
        self._p2 = list(player2)[0]
        self._p1c = list(player1)[1]
        self._p2c = list(player2)[1]
        self._p1res = 0
        self._p2res = 0
        self._p1cap = 0
        self._p2cap = 0
        self._turn = None
        self._gameboard = [[[self._p1c], [self._p1c], [self._p2c], [self._p2c], [self._p1c], [self._p1c]],
                           [[self._p2c], [self._p2c], [self._p1c], [self._p1c], [self._p2c], [self._p2c]],
                           [[self._p1c], [self._p1c], [self._p2c], [self._p2c], [self._p1c], [self._p1c]],
                           [[self._p2c], [self._p2c], [self._p1c], [self._p1c], [self._p2c], [self._p2c]],
                           [[self._p1c], [self._p1c], [self._p2c], [self._p2c], [self._p1c], [self._p1c]],
                           [[self._p2c], [self._p2c], [self._p1c], [self._p1c], [self._p2c], [self._p2c]]]

    def move_piece(self, player, start, end, pieces):
        """Moves a piece or pieces from a start position to an end position."""
        color = ""
        sp = list(start)                            # SP = Start positions
        ep = list(end)                              # EP = End positions
        r_change = sp[0] - ep[0]                     # Row change
        c_change = sp[1] - ep[1]                     # Column change
        total_change = abs(r_change)+abs(c_change)     # Absolute value of movement
        loc = self._gameboard[sp[0]][sp[1]]         # Location of Start position

        if color == "":
            if player == self._p1:
                color += self._p1c
            if player == self._p2:
                color += self._p2c

        return self.rule_check(player, color, sp, ep, pieces, r_change, c_change, total_change, loc)

    def rule_check(self, player, color, sp, ep, pieces, r_change, c_change, total_change, loc):
        """Checks the legality of potential moves"""
        if self.is_out_of_bounds(sp, ep) is True:
            return "Invalid location"

        # Diagonal moves
        if abs(r_change) >= 1 and abs(c_change) >= 1:
            return False

        # Not enough pieces exist in the location for the move
        if pieces > len(loc):
            return False

        # Trying to move the opponent's piece
        if loc[-1] != color:
            return "Invalid location"

        if self._turn is None or self._turn == color:
            if 1 < pieces <= len(loc):
                if total_change == pieces:
                    return self.multi_move(player, color, sp, ep, pieces)
                else:
                    return "Invalid number of pieces"
            if pieces == 1 and total_change == 1:
                return self.single_move(player, color, sp, ep)

        # The game is over
        if self._turn == 0:
            return False

        if self._turn != color:
            return "Not your turn"

    def is_out_of_bounds(self, sp, ep):
        """Checks if a move is out of bounds"""
        temp = sp + ep
        for i in temp:
            if 0 > i or i > 5:
                return True
        return False

    def multi_move(self, player, color, sp, ep, pieces):
        """A function that handles multiple piece movements"""
        holder = []

        # Adds pawns to holder and removes pawns from sp starting from the end.
        for pawn in range(0, pieces):
            holder.append(self._gameboard[sp[0]][sp[1]][-1])
            del self._gameboard[sp[0]][sp[1]][-1]

        # Adds pawns from holder starting from the end.
        for pawn in range(0, len(holder)):
            self._gameboard[ep[0]][ep[1]].append(holder[-1])
            del holder[-1]

        self.change_turn(color)
        return self.score_tally(player, color, ep)

    def single_move(self, player, color, sp, ep):
        """A function that handles single piece movements"""
        self._gameboard[ep[0]][ep[1]].append(self._gameboard[sp[0]][sp[1]][-1])
        del self._gameboard[sp[0]][sp[1]][-1]

        self.change_turn(color)
        return self.score_tally(player, color, ep)

    def score_tally(self, player, color, ep, capture=0, reserve=0):
        """A function adds captures and reserves, as well as declaring the winner."""
        length = len(self._gameboard[ep[0]][ep[1]])

        # Tallies reserves and captures from the first element.
        if length >= 6:
            for i in range(6, length + 1):
                if self._gameboard[ep[0]][ep[1]][0] == color:
                    reserve += 1
                else:
                    capture += 1
                del self._gameboard[ep[0]][ep[1]][0]
        return self.win_check(player, color, capture, reserve)

    def win_check(self, player, color, capture, reserve):
        """Checks if the moving player wins after their move is completed"""
        # Adds points, reserves, and checks for winners.
        if self._p1c == color:
            self._p1res += reserve
            self._p1cap += capture
            if self._p1cap > 5:
                self._turn = 0
                return player + " Wins!"

        if self._p2c == color:
            self._p2res += reserve
            self._p2cap += capture
            if self._p2cap > 5:
                self._turn = 0
                return player + " Wins!"

        return "successfully moved"

    def reserved_move(self, player, location):
        """A function that handles reserved movements"""
        color = ""
        ep = list(location)

        # ep is used twice, because it is the start and end point.
        if self.is_out_of_bounds(ep, ep) is True:
            return "Invalid Location"

        if color == "":
            if player == self._p1:
                color = self._p1c
                if self._turn == color:
                    if self._p1res > 0:
                        self._gameboard[ep[0]][ep[1]].append(color)
                        self._p1res -= 1
                    else:
                        return "No pieces in reserve"
                else:
                    return False

            if player == self._p2:
                color = self._p2c
                if self._turn == color:
                    if self._p2res > 0:
                        self._gameboard[ep[0]][ep[1]].append(color)
                        self._p2res -= 1
                    else:
                        return "No pieces in reserve"
                else:
                    return False

        self.change_turn(color)
        return self.score_tally(player, color, ep)

    def change_turn(self, color):
        """Changes whose turn it is."""
        # If it is the first turn, switches turn to current player's
        if self._turn is None:
            self._turn = color

        # Switches the turn from the current player to the opposing player
        if self._turn == self._p1c:
            self._turn = self._p2c
        else:
            self._turn = self._p1c

    def show_pieces(self, location):
        """Returns the pieces in a set location on the board."""
        row = list(location)[0]
        col = list(location)[1]
        return self._gameboard[row][col]

    def show_reserve(self, player):
        """Shows the number of reserve pieces a player has"""
        if player == self._p1:
            return self._p1res

        elif player == self._p2:
            return self._p2res

        else:
            return "Player not found."

    def show_captured(self, player):
        """Shows the number of pieces captured by the player"""
        if player == self._p1:
            return self._p1cap

        elif player == self._p2:
            return self._p2cap

        else:
            return "Player not found."

    def show_gameboard(self):
        """Prints the game board"""
        for i in range(0, len(self._gameboard)):
            print(self._gameboard[i])
#
#     def show_players(self):
#         """Shows who the players are, for testing purposes"""
#         return print(self._p1 + " and " + self._p2)
#
#     def test_add(self, position, color):
#         """For testing purposes, adds a color's pawn to a location"""
#         pos = list(position)
#         self._gameboard[pos[0]][pos[1]].append(color)
#         return print(color + " added successfully")
#
#
# game = FocusGame(('PlayerA', 'R'), ('PlayerB', 'G'))
#
# print("###Checks game board###")
# game.show_gameboard()
# game.show_pieces((0, 0))
# game.test_add((0, 0), 'R')
# game.test_add((0, 0), 'G')
# game.test_add((0, 0), 'G')
# game.test_add((0, 0), 'G')
# game.show_gameboard()
# game.show_pieces((0, 0))
#
# print("###Tests basic movement and unit reserve###")
# print(game.move_piece('PlayerA', (0, 1), (0, 0), 1))
# game.show_gameboard()
#
# print("###Tests turns###")
# print(game.move_piece("PlayerB", (1, 1), (1, 0), 1))
# print(game.move_piece("PlayerB", (1, 0), (1, 1), 1))
# print(game.move_piece("PlayerA", (0, 0), (0, 1), 1))
# print(game.move_piece("PlayerA", (0, 1), (0, 0), 1))
# print(game.move_piece("PlayerB", (1, 1), (1, 0), 1))
# print(game.move_piece("PlayerA", (0, 1), (0, 0), 1))
#
# print("###Tests multi move and capture###")
# game.test_add((0, 0), 'G')
# game.test_add((0, 0), 'G')
# game.test_add((0, 0), 'G')
# game.test_add((0, 0), 'R')
# game.test_add((5, 0), 'R')
# game.test_add((5, 0), 'G')
# game.test_add((5, 0), 'G')
# game.test_add((5, 0), 'G')
# game.show_gameboard()
# print(game.move_piece("PlayerA", (0, 0), (5, 0), 5))
# print(game.show_captured('PlayerA'))
# print(game.show_reserve('PlayerA'))
#
# print("###Tests Illegal Moves###")
# game.test_add((0, 0), 'R')
# game.test_add((0, 0), 'R')
# game.test_add((0, 0), 'R')
# game.test_add((0, 0), 'R')
# game.show_gameboard()
# print(game.move_piece("PlayerA", (0, 0), (0, 1), 5))
# print(game.move_piece("PlayerA", (0, 0), (6, 6), 5))
# print(game.move_piece("PlayerA", (1, 0), (1, 1), 1))
# print(game.move_piece("PlayerA", (0, 1), (0, 0), 2))
# print(game.move_piece("PlayerA", (0, 1), (0, 0), 1))  # Successful move here
#
# print("###Tests reserve move###")
# game.test_add((0, 0), 'R')
# game.test_add((0, 0), 'R')
# game.test_add((0, 0), 'R')
# game.test_add((0, 0), 'R')
# game.move_piece("PlayerA", (0, 1), (0, 0), 1)
# game.move_piece("PlayerB", (5, 5), (5, 4), 1)
# print(game.show_reserve('PlayerA'))
# print(game.show_pieces((5, 4)))
# game.reserved_move("PlayerA", (5, 4))
# print(game.show_reserve('PlayerA'))
# print(game.show_pieces((5, 4)))
#
# print("###Tests win and if the game stops after win###")
# game.test_add((0, 0), 'R')
# game.test_add((0, 0), 'R')
# game.test_add((0, 0), 'R')
# game.test_add((0, 0), 'R')
# game.test_add((0, 0), 'R')
# game.test_add((0, 0), 'R')
# game.test_add((0, 0), 'R')
# game.test_add((0, 0), 'R')
# game.test_add((0, 0), 'R')
# game.test_add((0, 0), 'R')
# game.test_add((0, 0), 'R')
# game.test_add((0, 0), 'R')
# game.show_gameboard()
# print(game.move_piece("PlayerB", (1, 0), (0, 0), 1))
# print(game.move_piece("PlayerA", (0, 1), (0, 0), 1))
