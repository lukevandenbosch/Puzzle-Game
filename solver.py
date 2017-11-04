# Assignment 2 - Puzzle Game
#
# CSC148 Summer 2017, University of Toronto
# ---------------------------------------------
"""This module contains functions responsible for solving a puzzle.

This module can be used to take a puzzle and generate one or all
possible solutions. It can also generate hints for a puzzle (see Part 4).
"""
from puzzle import Puzzle
from sudoku_puzzle import SudokuPuzzle
from word_ladder_puzzle import WordLadderPuzzle

def solve(puzzle, verbose=False):
    """Return a solution of the puzzle.

    Even if there is only one possible solution, just return one of them.
    If there are no possible solutions, return None.

    In 'verbose' mode, print out every state explored in addition to
    the final solution. By default 'verbose' mode is disabled.

    Uses a recursive algorithm to exhaustively try all possible
    sequences of moves (using the 'extensions' method of the Puzzle
    interface) until it finds a solution.

    @type puzzle: Puzzle
    @type verbose: bool
    @rtype: Puzzle | None
    """
    sol = puzzle.extensions()
    s = puzzle
    for i in sol:
        if verbose == True:
            print(i)
        if not i.is_solved():
            s = solve(i)
            if s != puzzle:
                break
        else:
            s = i
            break
    return s


def solve_complete(puzzle, verbose=False):
    """Return all solutions of the puzzle.

    Return an empty list if there are no possible solutions.

    In 'verbose' mode, print out every state explored in addition to
    the final solution. By default 'verbose' mode is disabled.

    Uses a recursive algorithm to exhaustively try all possible
    sequences of moves (using the 'extensions' method of the Puzzle
    interface) until it finds all solutions.

    @type puzzle: Puzzle
    @type verbose: bool
    @rtype: list[Puzzle]
    """
    sol = puzzle.extensions()
    s = []
    for i in sol:
        if verbose == True:
            print(i)
        if not i.is_solved():
            solu = solve_complete(i)
            for i in solu:
                s.append(i)
        else:
            s.append(i)
    return s

def extensions_at_depth(puzzle, n):
    """
    Return a list of all extensions that are arrived at from a puzzle. This is a helper
    function for hint_by_depth.
    
    Precondition: n >= 1.
    
    @type puzzle: Puzzle
    @type n: int
    @rtype: lst[Puzzle]
    """
    lst = []
    x = puzzle.extensions()
    if n == 1:
        return x
    for i in x:
        lst.append(i)
        if i.extensions() != None:
            y = extensions_at_depth(i,n-1)
            for j in y:
                lst.append(j)
    return lst

def hint_by_depth(puzzle, n):
    """Return a hint for the given puzzle state.
    Precondition: n >= 1.
    If <puzzle> is already solved, return the string ’Already at a solution!’
    If <puzzle> cannot lead to a solution or other valid state within <n> moves,
    return the string ’No possible extensions!’
    
    @type puzzle: Puzzle
    @type n: int
    @rtype: str
    """
    if puzzle.is_solved():
        return 'Already at a solution!'
    sol = extensions_at_depth(puzzle, n)
    ext = puzzle.extensions()
    n = 0
    for i in range(len(sol)):
        if sol[i].is_solved():
            while True:
                if sol[i-n] in ext:
                    return puzzle.move_finder(sol[i-n])
                else:
                    n += 1
    if sol == []:
        return 'No possible extensions!'

    return puzzle.move_finder(sol[0])


if __name__ == '__main__':
    pass
    