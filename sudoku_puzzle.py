# Assignment 2 - Puzzle Game
#
# CSC148 Summer 2017, University of Toronto
# ---------------------------------------------
"""Sudoku puzzle module.

Here are the rules of Sudoku:

- The puzzle consists of an n-by-n grid, where n = 4, 9, 16, or 25.
  Each square contains a uppercase letter between A and the n-th letter
  of the alphabet, or is empty.
  For example, on a 4-by-4 Sudoku board, the available letters are
  A, B, C, or D. On a 25-by-25 board, every letter A-Y is available.
- The goal is to fill in all empty squares with available letters so that
  the board has the following property:
    - no two squares in the same row have the same letter
    - no two squares in the same column have the same letter
    - no two squares in the same *subsquare* has the same letter
  A *subsquare* is found by dividing the board evenly into sqrt(n)-by-sqrt(n)
  pieces. For example, a 4-by-4 board would have 4 subsquares: top left,
  top right, bottom left, bottom right.

Note that most, but not all, of the code is given to you already.
"""
from puzzle import Puzzle
from math import sqrt
import copy

CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class SudokuPuzzle(Puzzle):
    """Implementation of a Sudoku puzzle."""
    # === Private Attributes ===
    # @type _n: int
    #     The size of the board. Must be 4, 9, 16, or 25.
    # @type _grid: list[list[str]]
    #     A representation of the Sudoku grid. Consists of a list of lists,
    #     where each inner list represents a row of the grid.
    #
    #     Each item of the inner list is either an uppercase letter,
    #     or is the empty string '', representing an empty square.
    #     Each letter must be between 'A' and the n-th letter of the alphabet.
    def __init__(self, grid):
        """Create a new Sudoku puzzle with an initial grid 'grid'.

        Precondition: <grid> is a valid Sudoku grid.

        @type self: SudokuPuzzle
        @type grid: list[list[str]]
        @rtype: None
        """
        self._n = len(grid)
        self._grid = grid

    def __str__(self):
        """Return a human-readable string representation of <self>.

        Note that the numbers at the top and left cycle 0-9,
        to help the user when they want to enter a move.

        @type self: SudokuPuzzle
        @rtype: str

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], ['D', 'C', 'B', 'A'], \
        ['', 'D', '', ''], ['', '', '', '']])
        >>> print(s)
          01|23
         ------
        0|AB|CD
        1|DC|BA
         ------
        2| D|
        3|  |
        <BLANKLINE>
        """
        m = int(sqrt(self._n))
        s = ''
        # Column label
        s += '  '
        for col in range(self._n):
            s += str(col % 10)
            # Vertical divider
            if (col + 1) % m == 0 and col + 1 != self._n:
                s += '|'
        # Horizontal divider
        s += '\n ' + ('-' * (self._n + m)) + '\n'
        for i in range(self._n):
            # Row label
            s += str(i % 10) + '|'
            for j in range(self._n):
                cell = self._grid[i][j]
                if cell == '':
                    s += ' '
                else:
                    s += str(cell)
                # Vertical divider
                if (j + 1) % m == 0 and j + 1 != self._n:
                    s += '|'
            s = s.rstrip()
            s += '\n'

            # Horizontal divider
            if (i + 1) % m == 0 and i + 1 != self._n:
                s += ' ' + ('-' * (self._n + m)) + '\n'

        return s
    def __eq__(self, other):
        """
        Return whether other is the same Sudoku Puzzle as self
        
        @type self: SudokuPuzzle
        @type other: SudokuPuzzle
        @rtype: bool
        """
        return self._grid == other._grid

    def is_solved(self):
        """Return whether <self> is solved.

        A Sudoku puzzle is solved if its state matches the criteria
        listed at the end of the puzzle description.

        @type self: SudokuPuzzle
        @rtype: bool

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'A', 'D', 'C'], \
                              ['D', 'C', 'B', 'A']])
        >>> s.is_solved()
        True
        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'D', 'A', 'C'], \
                              ['D', 'C', 'B', 'A']])
        >>> s.is_solved()
        False
        """
        # Check for empty cells
        for row in self._grid:
            if '' in row:
                return False

        # Check rows
        for row in self._grid:
            if sorted(row) != list(CHARS[:self._n]):
                return False

        # Check cols
        for i in range(self._n):
            # Note the use of a list comprehension here.
            if sorted([row[i] for row in self._grid]) != list(CHARS[:self._n]):
                return False

        # Check all subsquares
        m = int(sqrt(self._n))
        for x in range(0, self._n, m):
            for y in range(0, self._n, m):
                items = [self._grid[x + i][y + j]
                         for i in range(m)
                         for j in range(m)]

                if sorted(items) != list(CHARS[:self._n]):
                    return False

        # All checks passed
        return True

    def extensions(self):
        """Return list of extensions of <self>.

        This method picks the first empty cell (looking top-down,
        left-to-right) and returns a list of the new puzzle states
        obtained by filling in the empty cell with one of the
        available letters that does not violate any of the constraints
        listed in the problem description. (E.g., if there is
        already an 'A' in the row with the empty cell, this method should
        not try to fill in the cell with an 'A'.)

        If there are no empty cells, returns an empty list.

        @type self: SudokuPuzzle
        @rtype: list[SudokuPuzzle]

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'A', '', ''], \
                              ['D', 'C', '', '']])
        >>> lst = list(s.extensions())
        >>> len(lst)
        1
        >>> print(lst[0])
        
          01|23
         ------
        0|AB|CD
        1|CD|AB
         ------
        2|BA|D
        3|DC|
        
        <BLANKLINE>
        """
        # Search for the first empty cell
        row_index, col_index = None, None
        for i in range(self._n):
            row = self._grid[i]
            if '' in row:
                row_index, col_index = i, row.index('')
                break

        if row_index is None:
            return []
        else:
            # Calculate possible letter to fill the empty cell
            letters = self._possible_letters(row_index, col_index)
            return [self._extend(letter, row_index, col_index)
                    for letter in letters]

    # ------------------------------------------------------------------------
    # Helpers for method 'extensions'
    # ------------------------------------------------------------------------
    def _possible_letters(self, row_index, col_index):
        """Return a list of the possible letters for a cell.

        The returned letters must be a subset of the available letters.
        The returned list should be sorted in alphabetical order.

        @type self: SudokuPuzzle
        @type row_index: int
        @type col_index: int
        @rtype: list[str]
        """
        checkr = []
        checkc = []
        checksq = []
        subs = sqrt(self._n)
        rblock = subs*int(row_index/float(subs))
        cblock = subs*int(col_index/float(subs))
        lst = list(CHARS[:self._n])
        retlst = copy.copy(lst)
        for i, x in enumerate(self._grid):
            for j in range(len(x)):
                if i == row_index:
                    checkr.append(self._grid[i][j])
                if j == col_index:
                    checkc.append(self._grid[i][j])
                if rblock <= i < rblock + subs and cblock <= j < cblock + subs:
                    checksq.append(self._grid[i][j])
        for abc in lst:
            if abc in checkr or abc in checkc or abc in checksq:
                retlst.remove(abc)
        return retlst

    def _extend(self, letter, row_index, col_index):
        """Return a new Sudoku puzzle obtained after one move.

        The new puzzle is identical to <self>, except that it has
        the value at position (row_index, col_index) equal to 'letter'
        instead of empty.

        'letter' must be an available letter.
        'row_index' and 'col_index' are between 0-3.

        @type self: SudokuPuzzle
        @type letter: str
        @type row_index: int
        @type col_index: int
        @rtype: SudokuPuzzle

        >>> s = SudokuPuzzle([['A', 'B', 'C', 'D'], \
                              ['C', 'D', 'A', 'B'], \
                              ['B', 'A', '', ''], \
                              ['D', 'C', '', '']])
        >>> print(s._extend('B', 2, 3))
          01|23
         ------
        0|AB|CD
        1|CD|AB
         ------
        2|BA| B
        3|DC|
        <BLANKLINE>
        """
        new_grid = [row.copy() for row in self._grid]
        new_grid[row_index][col_index] = letter
        return SudokuPuzzle(new_grid)
    def move_finder(self, puzzle_end):
        """
        Find the move that has been made between self puzzle and the puzzle_end and return a string
        of that move in the form (<row>, <col>) -> <letter>
        
        Precondition: puzzle_end must be one valid move away from self
        
        @type self: SudokuPuzzle
        @type puzzle_end: SudokuPuzzle
        @rtype: str
        """
        str1 = '('
        str2 = ', '
        str3 = ') -> '
        for i in range(self._n):
            for j in range(self._n):
                for abc in list(CHARS[:self._n]):
                    if self._extend(abc, i, j) == puzzle_end:
                        return str1 + str(i) + str2 + str(j) + str3 + str(abc)
    def move(self, move):
        """
        change the state of the system to the new move
        if the move is invalid then raise an ValueError
        
        @type self: SudokuPuzzle
        @type move: str
            string in the form (<row>, <col>) -> <letter>
        """
        mov = list(move)
        num = list('1234567890')
        abc = []
        alpha = list(CHARS)
        for i in range(self._n):
            abc.append(alpha[i])
        len1 = 0
        condition1 = True
        len2 = 0
        condition2 = True
        if len(mov) == 0:
            raise ValueError("Invalid Input Error")
        if mov[0] != '(':
            raise ValueError("Invalid Input Error")
        while condition1:
            if not mov[1+len1] in num:
                raise ValueError("Invalid Input Error")
            if mov[2+len1] in num:
                len1 += 1
            elif mov[2+len1] == ',':
                condition1 = False
            else:
                raise ValueError("Invalid Input Error")
        if mov[3+len1] != ' ':
            raise ValueError("Invalid Input Error")
        while condition2:
            if not mov[4+len1+len2] in num:
                raise ValueError("Invalid Input Error")
            if mov[5+len1+len2] in num:
                len2 += 1
            elif mov[5+len1+len2] == ')':
                condition2 = False
            else:
                raise ValueError("Invalid Input Error")
        if mov[6+len1+len2] != ' ' or mov[7+len1+len2] != '-' or mov[8+len1+len2] != '>' or mov[9+len1+len2] != ' ':
            raise ValueError("Invalid Input Error")
        if not mov[10+len1+len2] in abc:
            raise ValueError("Invalid Input Error")
        xpos = ''
        ypos = ''
        for i in range(len1+1):
            xpos += mov[1+i]
        for j in range(len2+1):
            ypos += mov[4+len1+j]
        pos = (int(xpos),int(ypos))
        let = mov[10+len1+len2]
        if not let in self._possible_letters(pos[0], pos[1]):
            raise ValueError("Invalid Input Error Cannot Put This Letter Here")
        return self._extend(let,pos[0],pos[1])
        

if __name__ == '__main__':
    '''# Note: the doctest of 'extensions' currently fails. See Part 1.
    import doctest
    doctest.testmod()'''

    # Here is a bigger Sudoku puzzle
    '''big = SudokuPuzzle(
        [['E', 'C', '', '', 'G', '', '', '', ''],
         ['F', '', '', 'A', 'I', 'E', '', '', ''],
         ['', 'I', 'H', '', '', '', '', 'F', ''],
         ['H', '', '', '', 'F', '', '', '', 'C'],
         ['D', '', '', 'H', '', 'C', '', '', 'A'],
         ['G', '', '', '', 'B', '', '', '', 'F'],
         ['', 'F', '', '', '', '', 'B', 'H', ''],
         ['', '', '', 'D', 'A', 'I', '', '', 'E'],
         ['', '', '', '', 'H', '', '', 'G', 'I']]
    )'''
    s = SudokuPuzzle([['A', 'B', 'C', 'D'],
                      ['C', 'D', 'A', 'B'],
                      ['B', 'A', '', ''],
                      ['D', 'C', '', '']])
    
