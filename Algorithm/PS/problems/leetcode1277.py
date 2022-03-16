1. class Solution:
2.     def countSquares(self, matrix: List[List[int]]) -> int:
3.         if matrix is None or len(matrix) == 0:
4.             return 0
5.         
6.         rows = len(matrix)
7.         cols = len(matrix[0])
8.         
9.         result = 0
10.         
11.         for r in range(rows):
12.             for c in range(cols):
13.                 if matrix[r][c] == 1:   
14.                     if r == 0 or c == 0: # Cases with first row or first col
15.                         result += 1      # The 1 cells are square on its own               
16.                     else:                # Other cells
17.                         cell_val = min(matrix[r-1][c-1], matrix[r][c-1], matrix[r-1][c]) + matrix[r][c]
18.                         result += cell_val
19.                         matrix[r][c] = cell_val #**memoize the updated result**
20.         return result