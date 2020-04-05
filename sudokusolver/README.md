# Sudoku

A sudoku board is an 9x9 array of integers. All empty cells are filled with 0s.

Below is an example of how to initialize a board, a solver, and solver the problem.

```python
import sudoku, backtracking
s = sudoku.SudokuBoard([[2, 0, 0, 4, 0, 1, 0, 0, 5], [0, 7, 0, 0, 5, 0, 0, 4, 0], [5, 9, 0, 0, 3, 0, 0, 6, 8], [0, 0, 8, 3, 4, 6, 7, 0, 0], [0, 1, 0, 9, 0, 2, 0, 5, 0], [3, 0, 2, 0, 7, 0, 6, 0, 9], [0, 2, 9, 0, 0, 0, 8, 3, 0], [0, 0, 5, 0, 2, 0, 4, 0, 0], [4, 0, 0, 6, 9, 8, 0, 0, 7]])
solver = backtracking.SudokuSolver1(s)
solver.Solve()
```
