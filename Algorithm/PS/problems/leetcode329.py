    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        rows, cols = len(matrix), len(matrix[0])
        dp = [[0 for _ in range(cols)] for _ in range(rows)]
        
        def dfs(i, j):
            if not dp[i][j]:
                val = matrix[i][j]
								# 
                dp[i][j] = 1 + max(
                    dfs(i+1, j) if i+1 < rows and val > matrix[i+1][j] else 0,
                    dfs(i, j+1) if j+1 < cols and val > matrix[i][j+1] else 0,
                    dfs(i-1, j) if i-1 >= 0 and val > matrix[i-1][j] else 0,
                    dfs(i, j-1) if j-1 >= 0 and val > matrix[i][j-1] else 0
                )
            return dp[i][j]
        
        ans = max([dfs(i, j) for i in range(rows) for j in range(cols)])
        return ans