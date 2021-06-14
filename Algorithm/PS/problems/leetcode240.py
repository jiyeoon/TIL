class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        for row in matrix:
            try:
                idx = row.index(target)
                if idx != -1:
                    return True
            except:
                continue
        return False