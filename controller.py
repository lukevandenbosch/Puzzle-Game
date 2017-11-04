# Assignment 2 - Puzzle Game
#
# CSC148 Summer 2017, University of Toronto
# ---------------------------------------------
"""Module containing the Controller class."""
from view import TextView, WebView
from puzzle import Puzzle
from solver import solve, solve_complete, hint_by_depth

class StateTree:
    """
    Implement a class that is a tree of the states explored in the runtime of the game
    """
    
    def __init__(self, root = None, children = None):
        """
        Initialize the state tree start with no roots and no children
        
        @type self: StateTree
        @type root: Puzzle
        @type children: list[Puzzle]
        @rtype: None
        """
        self.root = root
        self.children = children.copy() if children else []
        
    def __eq__(self, Other):
        """
        Create an equals meathod where you can check if one StateTree is othe same as another StateTree
        
        @type self: StateTree
        @type Other: StateTree
        @rtype: bool
        """
        return (type(self) is type(Other) and self.children == Other.children and self.root == Other.root)
    def __str__(self, indent=0):
        """
        Produce a user-friendly string representation of Tree self,
        indenting each level as a visual clue.

        @type self: StateTree
        @type indent: int 
        @rtype: str
        """
        root_str = indent * " " + str(self.root)
        return '\n'.join([root_str] +
                         [c.__str__(indent + 3) for c in self.children])
    def node_list(self):
        """
        Create a list of every node in the entire tree to be a helper function for put_item and find_par
        
        @type self: StateTree
        @rtype: list[StateTree]
        """
        lst = [self]
        for i in self.children:
            if len(i.children) == 0:
                lst.append(i)
            else:
                ind = i.node_list()
                for j in ind:
                    lst.append(j)
        return lst
    def put_item(self, item, parent):
        """
        Create a function to put an item into the StateTree based on its' parent
        
        Preconditions:
            - item must be a 2 tuple of the newly moved Puzzle with the input string of the user
            - parent must be the initial Puzzle
        
        @type self: StateTree
        @type item: (Puzzle, str)
        @type parent: Puzzle
        @rtype: None
        """
        lst = self.node_list()
        swit = 0
        for i in lst:
            if parent == i.root[0]:
                for j in i.children:
                    if j.root == item:
                        swit += 1
                if swit == 0:
                    i.children.append(StateTree(item))
    def find_par(self, item):
        """
        Find the parent of the item presented
        
        Preconditions:
            - item is a Puzzle to help in the :UNDO function
        
        @type self: StateTree
        @type item: Puzzle
        @rtype: Puzzle
        """
        lst = self.node_list()
        parent = None
        node =  None
        index = 0
        for i in range(len(lst)):
            if lst[i].root[0] == item:
                if i == 0:
                    return parent
                index = i
                node = lst[i]
                parent = lst[i-1]
        while True:
            if node in parent.children:
                return parent
            else:
                index -= 1
                parent = lst[index-1]

abc = 'abcdefghijklmnopqrstuvwxyz'

class Controller:
    """Class responsible for connection between puzzles and views.

    You may add new *private* attributes to this class to help you
    in your implementation.
    """
    # === Private Attributes ===
    # @type _puzzle: Puzzle
    #     The puzzle associated with this game controller
    # @type _tree: StateTree
    #     The State tree of the system.
    # @type _view: View
    #     The view associated with this game controller

    def __init__(self, puzzle, mode='text'):
        """Create a new controller.

        <mode> is either 'text' or 'web', representing the type of view
        to use.

        By default, <mode> has a value of 'text'.

        @type puzzle: Puzzle
        @type mode: str
        @rtype: None
        """
        self._puzzle = puzzle
        self._tree = StateTree((self._puzzle, ''))
        if mode == 'text':
            self._view = TextView(self)
        elif mode == 'web':
            self._view = WebView(self)
        else:
            raise ValueError()

        # Start the game.
        self._view.run()

    def state(self):
        """Return a string representation of the current puzzle state.

        @type self: Controller
        @rtype: str
        """
        return str(self._puzzle)

    def act(self, action):
        """Run an action represented by string <action>.

        Return a string representing either the new state or an error message,
        and whether the program should end.

        @type self: Controller
        @type action: str
        @rtype: (str, bool)
        """        
        if action == ':EXIT':
            return ('', True)
        elif action == ':SOLVE':
            return (solve(self._puzzle), True)
        elif action == ':SOLVE-ALL':
            return (solve_complete(self._puzzle), True)
        elif list(action)[0] == '(' and list(action)[-6:-1] == list(') -> '):
            newp = self._puzzle.move(action)
            self._tree.put_item((newp, action),self._puzzle)
            self._puzzle = newp
            return (newp, newp.is_solved())
        elif [x for x in list(abc) if x in list(action)]:
            newp = self._puzzle.move(action)
            self._tree.put_item((newp, action),self._puzzle)
            self._puzzle = newp
            return (newp, newp.is_solved())
        elif action == ':UNDO':
            parent = self._tree.find_par(self._puzzle)
            if parent != None:
                self._puzzle = parent.root[0]
            else:
                print("The previous state does not exist.")
            return (self._puzzle, self._puzzle.is_solved())
        elif action == ':ATTEMPTS':
            lst = self._tree.node_list()
            for i in range(len(lst)):
                if i != 0:
                    print(i.root[1])
                    print('----------------')
                    print(i.root[0])
            return (self.state(), False)
        elif list(action)[:5] == list(':HINT'):
            num = ''
            for i in range(len(list(action))-6):
                num += action[6+i]
            x = hint_by_depth(self._puzzle, int(num))
            if x == 'No possible extensions!' or x == 'Already at a solution!':
                print(x)
                return (self.state(), False)
            return (x, self._puzzle.is_solved())
        else:
            return (self.state(), False)



if __name__ == '__main__':
    from sudoku_puzzle import SudokuPuzzle
    from word_ladder_puzzle import WordLadderPuzzle

    s = SudokuPuzzle([['', '', '', ''],
                      ['', '', '', ''],
                      ['C', 'D', 'A', 'B'],
                      ['A', 'B', 'C', 'D']])
    #w = WordLadderPuzzle('mare','core')
    c = Controller(s)

