class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        total = len(matrix) * len(matrix[0])
        directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        
        dir_idx = 0
        
        visited = set()
        
        curr_i, curr_j = 0, 0
        res = []
        while True:
            res.append(matrix[curr_i][curr_j])
            visited.add((curr_i, curr_j))
            
            # 다음에 갈 애
            nxt_i, nxt_j = curr_i + directions[dir_idx][0], curr_j + directions[dir_idx][1]
            
            if (0 <= nxt_i < len(matrix) and 0 <= nxt_j < len(matrix[0])) and (nxt_i, nxt_j) not in visited:
                curr_i, curr_j = nxt_i, nxt_j
            else:
                # 1. 끝내야하는 경우
                if len(visited) == total:
                    return res
                
                # 2. 방향을 바꿔야하는 경우 
                dir_idx = (dir_idx + 1) % 4
                nxt_i, nxt_j = curr_i + directions[dir_idx][0], curr_j + directions[dir_idx][1]
                if (0 <= nxt_i < len(matrix) and 0 <= nxt_j < len(matrix[0])):
                    curr_i, curr_j = nxt_i, nxt_j
                else:
                    break
                
        return res


        