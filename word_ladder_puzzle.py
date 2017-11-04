# Assignment 2 - Puzzle Game
#
# CSC148 Summer 2017, University of Toronto
# ---------------------------------------------
"""Word ladder module.

Your task is to complete the implementation of this class so that
you can use it to play Word Ladder in your game program.

Rules of Word Ladder
--------------------
1. You are given a start word and a target word (all words in this puzzle
   are lowercase).
2. Your goal is to reach the target word by making a series of *legal moves*,
   beginning from the start word.
3. A legal move at the current word is to change ONE letter to get
   a current new word, where the new word must be a valid English word.

The sequence of words from the start to the target is called
a "word ladder," hence the name of the puzzle.

Example:
    Start word: 'make'
    Target word: 'cure'
    Solution:
        make
        bake
        bare
        care
        cure

    Note that there are many possible solutions, and in fact a shorter one
    exists for the above puzzle. Do you see it?

Implementation details:
- We have provided some starter code in the constructor which reads in a list
  of valid English words from wordsEn.txt. You should use this list to
  determine what moves are valid.
- **WARNING**: unlike Sudoku, Word Ladder has the possibility of getting
  into infinite recursion if you aren't careful. The puzzle state
  should keep track not just of the current word, but all words
  in the ladder. This way, in the 'extensions' method you can just
  return the possible new words which haven't already been used.
"""
import copy
from puzzle import Puzzle


CHARS = 'abcdefghijklmnopqrstuvwyz'


class WordLadderPuzzle(Puzzle):
    """A word ladder puzzle."""
    # TODO: add to this list of private attributes!
    # === Private attributes ===
    # @type _words: list[str]
    #     List of allowed English words

    def __init__(self, start, target):
        """Create a new word ladder puzzle with given start and target words.

        Note: you may add OPTIONAL arguments to this constructor,
        but you may not change the purpose of <start> and <target>.

        @type self: WordLadderPuzzle
        @type start: str
        @type target: str
        @rtype: None
        """
        # Code to initialize _words - you don't need to change this.
        self._words = []
        with open('wordsEn.txt') as wordfile:
            for line in wordfile:
                self._words.append(line.strip())

        self.start = start
        self.target = target
        self._hist = [start]

    def __str__(self):
        """
        Return a string of every move that is made in the word ladder puzzle
        
        @type self: WordLadderPuzzle
        @rtype: str
        """
        return ' '.join(self._hist)

    def is_solved(self):
        """
        return if the WordLadderPuzzle is solved
        
        @type self: WordLadderPuzzle
        @rtype: bool
        """
        return self.start == self.target
    
    def __eq__(self, other):
        """
        return if the other and self are equal
        
        @type self: WordLadderPuzzle
        @type other: WordLadderPuzzle
        @rtype: bool
        """
        return self.start == other.start and self.target == other.target

    def extensions(self):
        """Return a list of possible new states after a valid move.

        The valid move must change exactly one character of the
        current word, and must result in an English word stored in
        self._words.

        You should *not* perform any moves which produce a word
        that is already in the ladder.

        The returned moves should be sorted in alphabetical order
        of the produced word.

        @type self: WordLadderPuzzle
        @rtype: list[WordLadderPuzzle]
        """
        lst = []
        lst2 = []
        word = list(self.start)
        wordcopy = copy.copy(word)
        check = list(CHARS)
        for i in range(len(word)):
            for j in check:
                wordcopy[i] = j
                if "".join(wordcopy) in self._words and not "".join(wordcopy) in self._hist:
                    lst.append("".join(wordcopy))
                wordcopy = copy.copy(word)
        sort = sorted(lst)
        for i in sort:
            worr = WordLadderPuzzle(i,self.target)
            newhist = copy.copy(self._hist)
            newhist.append(i)
            worr._hist = newhist
            lst2.append(worr)
        return lst2
    def move_finder(self, puzzle_end):
        """
        find the string that was made previously with the puzzle_end
        
        @type self: WordLadderPuzzle
        @type puzzle_end: WordLadderPuzzle
        @rtype: str
        """
        return puzzle_end._hist[-1]
    def move(self, move):
        """
        Make a move and return the state of the system
        
        @type self: WordLadderPuzzle
        @type move: str
        @rtype: WordLadderPuzzle
        """
        ext = self.extensions()
        moves = []
        for i in ext:
            moves.append(i.start)
        if not move in moves:
            raise ValueError("Invalid Word")
        word = WordLadderPuzzle(move,self.target)
        newhist = copy.copy(self._hist)
        newhist.append(move)
        word._hist = newhist
        return word

