'''
그냥 문제 그대로 풀면 되는 문제..
1. 0인 좌표들을 먼저 찾고
2. 0인 좌표들을 하나하나 보면서 해당 좌표의 행과 열의 모든 좌표들을 0으로 바꿔준다
'''
class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        m, n = len(matrix), len(matrix[0])
        
        zeros = []
        for i in range(m):
            for j in range(n):
                if matrix[i][j] == 0:
                    zeros.append([i, j])
        
        for zero in zeros:
            row, col = zero
            
            # 해당 행의 모든 좌표들을 0으로 셋팅
            for j in range(n):
                matrix[row][j] = 0
            
            # 해당 열의 모든 좌표들을 0으로 셋팅
            for i in range(m):
                matrix[i][col] = 0
        
        return