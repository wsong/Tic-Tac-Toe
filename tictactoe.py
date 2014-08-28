#!/usr/bin/python

import copy

PLAYER_ONE = 'x'
PLAYER_TWO = 'o'

# Note that the minimax algorithm depends upon these values being positive,
# negative, and 0, respectively.
PLAYER_ONE_WIN_VALUE = 1
PLAYER_TWO_WIN_VALUE = -1
TIE_VALUE = 0


class BoardState(object):
  board = None
  value = None

  def __init__(self, board_size=3):
    """Initializes a BoardState object.

    Args:
      board_size: A positive integer.
    """
    self.board = []
    for i in range(board_size):
      self.board.append([None] * board_size)

  def __str__(self):
    # We add two spaces here so that the index for the first column (i.e. '1')
    # is correctly printed above the first column's space.
    s = '  '
    # Print the indices of the columns at the top.
    for i in range(1, len(self.board) + 1):
      s += str(i) + ' '
    s += '\n'
    for i in range(len(self.board)):
      # Print a, b, or c next to each row.
      s += chr(ord('a') + i) + ' '
      for j in range(len(self.board[i])):
        s += self.board[i][j] if self.board[i][j] else ' '
        if j != len(self.board[i]) - 1:
          s += '|'
      if i != len(self.board) - 1:
        # As above, we add two spaces here.
        s += '\n  '
        s += '_ ' * len(self.board)
        s += '\n'
    return s

  def make_move(self, move, player):
    """Makes a move for the given player.

    Args:
      move: A 2-tuple of the form (row, column) where row and column are
          0-based indices.
      player: Either PLAYER_ONE or PLAYER_TWO.
    """
    row, column = move
    self.board[row][column] = player
    self.update_value()

  def get_valid_board_states(self, player):
    """Get the valid board states for a given player's move.

    Args:
      player: Either PLAYER_ONE or PLAYER_TWO.
    Returns:
      A list of BoardState objects which represent board states that can be
          created when the given player makes a valid move on this board.
    """
    board_states = []
    for i in range(len(self.board)):
      for j in range(len(self.board[i])):
        if self.board[i][j] is None:
          new_board_state = copy.deepcopy(self)
          new_board_state.make_move((i, j), player)
          board_states.append(new_board_state)
    return board_states

  def update_value(self):
    """Updates the value of this board.

    Sets the .value field of this BoardState to PLAYER_ONE_WIN_VALUE if this is
    a winning board for player one, PLAYER_TWO_WIN_VALUE if this is a winning
    board for player two, TIE_VALUE if this is a tie, and None otherwise.
    """
    board_size = len(self.board)
    for row in self.board:
      # Check if either player has won by completing a row.
      if all(cell == PLAYER_ONE for cell in row):
        self.value = PLAYER_ONE_WIN_VALUE
        return
      elif all(cell == PLAYER_TWO for cell in row):
        self.value = PLAYER_TWO_WIN_VALUE
        return
    for i in range(board_size):
      # Check if either player has won by completing a column.
      if all(row[i] == PLAYER_ONE for row in self.board):
        self.value = PLAYER_ONE_WIN_VALUE
        return
      elif all(row[i] == PLAYER_TWO for row in self.board):
        self.value = PLAYER_TWO_WIN_VALUE
        return
    # Check if either player has won by completing a diagonal.
    if all(self.board[i][i] == PLAYER_ONE for i in range(board_size)):
      self.value = PLAYER_ONE_WIN_VALUE
      return
    elif all(self.board[i][i] == PLAYER_TWO for i in range(board_size)):
      self.value = PLAYER_TWO_WIN_VALUE
      return
    elif all(self.board[board_size - i - 1][i] == PLAYER_ONE
             for i in range(board_size)):
      self.value = PLAYER_ONE_WIN_VALUE
      return
    elif all(self.board[board_size - i - 1][i] == PLAYER_TWO
             for i in range(board_size)):
      self.value = PLAYER_TWO_WIN_VALUE
      return
    for row in self.board:
      if any(cell is None for cell in row):
        # If no player has won and there are any unset cells, the game isn't
        # over.
        self.value = None
        return
    # If there are no free spaces yet and no player has won, it's a tie.
    self.value = 0
    return


def _minimax_with_alpha_beta(board_state, alpha, beta, player):
  if board_state.value is not None:
    return board_state.value
  if player == PLAYER_ONE:
    next_board_states = board_state.get_valid_board_states(PLAYER_ONE)
    for next_board_state in next_board_states:
      alpha = max(
        alpha,
        _minimax_with_alpha_beta(next_board_state, alpha, beta, PLAYER_TWO))
      if beta <= alpha:
        break
    return alpha
  else:
    next_board_states = board_state.get_valid_board_states(PLAYER_TWO)
    for next_board_state in next_board_states:
      beta = min(
        beta,
        _minimax_with_alpha_beta(next_board_state, alpha, beta, PLAYER_ONE))
      if beta <= alpha:
        break
    return beta


def minimax(board_state, player):
  """Finds the best possible value of the given board state for a player.

  Args:
    board_state: A BoardState object.
    player: Either PLAYER_ONE or PLAYER_TWO.
  Returns:
    The best value the given player can achieve with this board if it is their
        turn to make a move and the other player plays perfectly.  This can be
        PLAYER_ONE_WIN_VALUE, PLAYER_TWO_WIN_VALUE, or TIE_VALUE.
  """
  return _minimax_with_alpha_beta(
    board_state, float('-inf'), float('inf'), player)


def get_player_move(board_state):
  """Gets a move from a human player.

  Args:
    board_state: A BoardState object.
  Returns:
    A (row, column) tuple indicating the cell in which the player wishes to
        place their piece.
  """
  player_move = None
  board_size = len(board_state.board)
  while player_move is None:
    move_input = raw_input('Enter your move: ')
    # Validate that the input is in the form <row><column>, where row is a
    # lowercase letter in the proper range and column is an integer, e.g.
    # 'a2'.
    if len(move_input) != 2:
      print 'Please enter a valid move.'
      continue
    if (not move_input[0].islower() or
        not ord(move_input[0]) in range(ord('a'), ord('a') + board_size)):
      print 'Please enter a valid move.'
      continue
    if (not move_input[1].isdigit() or
        not int(move_input[1]) in range(1, board_size + 1)):
      print 'Please enter a valid move.'
      continue
    row = ord(move_input[0]) - ord('a')
    column = int(move_input[1]) - 1
    if board_state.board[row][column] is not None:
      print 'That spot is taken.  Please enter a valid move.'
      continue
    player_move = (row, column)
  return player_move


def get_victory_text(board_state):
  if board_state.value == PLAYER_ONE_WIN_VALUE:
    return str(board_state) + '\n' + 'You win!'
  elif board_state.value == PLAYER_TWO_WIN_VALUE:
    return str(board_state) + '\n' + 'Computer wins!'
  elif board_state.value == TIE_VALUE:
    return str(board_state) + '\n' + 'It\'s a tie!'
  return None


def play_tic_tac_toe():
  board_state = BoardState(board_size=3)
  while board_state.value is None:
    print board_state
    player_move = get_player_move(board_state)
    board_state.make_move(player_move, PLAYER_ONE)
    victory_text = get_victory_text(board_state)
    if victory_text:
      print victory_text
      return
    next_board_states = board_state.get_valid_board_states(PLAYER_TWO)
    best_board_state = None
    best_value = float('inf')
    for next_board_state in next_board_states:
      value = minimax(next_board_state, PLAYER_ONE)
      if value < best_value:
        best_board_state = next_board_state
        best_value = value
    board_state = best_board_state
    victory_text = get_victory_text(board_state)
    if victory_text:
      print victory_text
      return


if __name__ == '__main__':
  print 'Welcome to Tic-Tac-Toe!'
  print ('You are X.  Please input your moves in the '
         'form <row><column>, e.g. \'b3\'.')
  play_tic_tac_toe()
