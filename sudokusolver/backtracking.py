from numpy import array
"""
"""

class SudokuSolver1(object):
    """Method:

    - Sweep through the board from left to right, top to bottom. 
    - Fill an empty cell with the smallest valid number, then go on.
    - If not possible to go on anymore, move back and increase the number by one, and continue.

    """

    def __init__(self, board):
        # An instance of a sudoku board
        self._board = board
        if not self._board.IsValid():
            raise ValueError('The input board is invalid: %s'%board)

        # Keep track of the initial condition.
        self._initialboarddata = array(self._board._data, dtype=int)

        # Initialize icurrentrow and icurrentcolumn to be the first empty cell
        self._icurrentrow = 0
        self._icurrentcolumn = 0
        if self._board[self._icurrentrow][self._icurrentcolumn] > 0:
            self._icurrentrow, self._icurrentcolumn = self.GetNextEmptyCell(self._icurrentrow, self._icurrentcolumn)


    def IsCellGiven(self, irow, icolumn):
        return self._initialboarddata[irow][icolumn] != 0


    def GetNextCell(self, irow, icolumn):
        if irow == 8 and icolumn == 8:
            return -1, -1 # reached the end of the board

        if icolumn == 8:
            irow += 1
        icolumn = (icolumn + 1) % 9
        return irow, icolumn


    def GetPreviousCell(self, irow, icolumn):
        if irow == 0 and icolumn == 0:
            return -1, -1 # reached the end of the board

        if icolumn == 0:
            irow -= 1
        icolumn = (icolumn - 1) % 9
        return irow, icolumn


    def GetNextEmptyCell(self, irow, icolumn):
        newirow, newicolumn = self.GetNextCell(irow, icolumn)
        while self.IsCellGiven(newirow, newicolumn):
            newirow, newicolumn = self.GetNextCell(newirow, newicolumn)
            if newirow == -1 and newicolumn == -1:
                break
        return newirow, newicolumn


    def GetPreviousEmptyCell(self, irow, icolumn):
        newirow, newicolumn = self.GetPreviousCell(irow, icolumn)
        while self.IsCellGiven(newirow, newicolumn):
            newirow, newicolumn = self.GetPreviousCell(newirow, newicolumn)
            if newirow == -1 and newicolumn == -1:
                break
        return newirow, newicolumn


    def Solve(self):
        """
        
        """
        numiter = 0
        while self._icurrentrow != -1 and self._icurrentcolumn != -1:
            numiter += 1
            print 'it=%d: currow=%d; curcol=%d; curval=%d'%(numiter, self._icurrentrow, self._icurrentcolumn, self._board[self._icurrentrow][self._icurrentcolumn])
            
            if self._board[self._icurrentrow][self._icurrentcolumn] < 9:
                self._board[self._icurrentrow][self._icurrentcolumn] += 1
            else:
                # Cannot go further. Reset this cell and move back.
                self._board[self._icurrentrow][self._icurrentcolumn] = 0
                self._icurrentrow, self._icurrentcolumn = self.GetPreviousEmptyCell(self._icurrentrow, self._icurrentcolumn)
                continue
                
            iregion = self._board.GetRegionIndexFromRowColumn(self._icurrentrow, self._icurrentcolumn)
            if not self._board.IsRegionValid(iregion):
                print '    iregion=%d is invalid'%(iregion)
                continue

            if not self._board.IsCellValid(self._icurrentrow, self._icurrentcolumn):
                print '    cell (%d, %d) is invalid'%(self._icurrentrow, self._icurrentcolumn)
                continue

            # This change is fine so far, so move forward
            self._icurrentrow, self._icurrentcolumn = self.GetNextEmptyCell(self._icurrentrow, self._icurrentcolumn)
            continue

        if self._board.IsSolved:
            return True

        else:
            # The board is invalid, so cannot be solved.
            return False
