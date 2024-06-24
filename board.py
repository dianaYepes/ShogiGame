import os


class Board:
    """
    Class that represents the board
    """

    # The BoxShogi board is 5x5
    BOARD_SIZE = 5

    def __init__(self, mode='file'):
        if mode == '-i':
            self._board = self._initInteractiveBoard()
        else:
            self._board = self._initEmptyBoard()
            

    def _initEmptyBoard(self):
        # TODO: Initalize empty board for file mode
        return [
            ['__','__','__','__','__'],
            ['__','__','__','__','__'],
            ['__','__','__','__','__'],
            ['__','__','__','__','__'],
            ['__','__','__','__','__']]
        # list = [['__'] for _ in range(5)]
    
    def _initInteractiveBoard(self):
         # TODO: Initalize starting board for interactive mode
        return [
            [' d',' p','__','__',' N'],
            [' s','__','__','__',' G'],
            [' r','__','__','__',' R'],
            [' g','__','__','__',' S'],
            [' n','__','__',' P',' D']]

    def __repr__(self):
        return self._stringifyBoard()

    def _stringifyBoard(self):
        """
        Utility function for printing the board
        """
        s = ''
        for row in range(len(self._board) - 1, -1, -1):

            s += '' + str(row + 1) + ' |'
            for col in range(0, len(self._board[row])):
                s += self._stringifySquare(self._board[col][row])

            s += os.linesep

        s += '    a  b  c  d  e' + os.linesep
        return s

    def _stringifySquare(self, sq):
        """
       	Utility function for stringifying an individual square on the board

        :param sq: Array of strings.
        """
        if type(sq) is not str or len(sq) > 2:
            raise ValueError('Board must be an array of strings like "", "P", or "+P"')
        if len(sq) == 0:
            return '__|'
        if len(sq) == 1:
            return ' ' + sq + '|'
        if len(sq) == 2:
            return sq + '|'
        

    def updateBoard(self, pos, pieceString):
        self._board[pos[0]][pos[1]] = pieceString
