from collections import Counter
from numpy import array

class SudokuBoard(object):

    # SudokuBoard is a class representing a 9x9 sudoku puzzle. The argument for initializing this class is a 9x9 array
    # filled with numbers 0 -- 9. The empty cells left blank for players to fill are represented by 0s.
    def __init__(self, data):
        self._data = array(data, dtype=int)


    def __str__(self):
        return self._data.__str__()


    def __repr__(self):
        return self._data.__repr__()


    def GetRow(self, irow):
        return self._data[irow]


    def GetColumn(self, icolumn):
        return self._data[:, icolumn]


    def GetRegion(self, iregion):
        istartrow = 3 * (int(iregion)/3)
        istartcolumn = 3*(iregion - istartrow)
        return self._data[istartrow: istartrow + 3, istartcolumn: istartcolumn + 3]        
        
    
    def IsValid(self):
        for iregion in xrange(9):
            if not self.IsRegionValid(iregion):
                return False
            
        for icolumn in xrange(9):
            for irow in xrange(9):
                if not self.IsCellValid(irow, icolumn):
                    return False
            # end for irow
        # end for icolumn
        return True
            

    def IsCellValid(self, irow, icolumn):
        # Only check its corresponding row and column
        if not self.IsRowValid(irow):
            return False

        if not self.IsColumnValid(icolumn):
            return False

        return True


    def IsRowValid(self, irow):
        cntr = Counter(self.GetRow(irow))
        return self._IsCounterValid(cntr)


    def IsColumnValid(self, icolumn):
        cntr = Counter(self.GetColumn(icolumn))
        return self._IsCounterValid(cntr)
    

    def GetRegionIndexFromRowColumn(self, irow, icolumn):
        return 3*(int(irow)/3) + icolumn/3

    
    def IsRegionValid(self, iregion):
        cntr = Counter(self.GetRegion(iregion).flatten())
        return self._IsCounterValid(cntr)

    
    def _IsCounterValid(self, cntr):
        for num in xrange(1, 10):
            if cntr[num] > 1:
                return False
            
        return True
        

    def IsSolved(self):
        if 0 in self._data:
            return False

        return self.IsBoardValid()
