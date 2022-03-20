class Solution:
    def minFlips(self, mat: List[List[int]]) -> int:
        visited = set()
        vector = []
        for row in mat:
            for d in row:
                vector.append(d)
        visited = set()
        visited.add(''.join(str(e) for e in vector))
        queue = [vector]
        flip = 0
        while queue:
            level_len = len(queue)
            for i in range(level_len):
                this_vec = queue.pop(0)
                if sum(this_vec) == 0:
                    return flip
                for i in range(len(this_vec)):
                    next_vec = self.flip(this_vec, i, len(mat[0]))
                    next_str = ''.join(str(e) for e in next_vec)
                    if next_str not in visited:
                        queue.append(next_vec)
                        visited.add(''.join(str(e) for e in next_vec))
            flip += 1
        return -1
    
    def flip(self, vec, i, row_len):
        ans = vec[:]
        ans[i] = 0 if ans[i] == 1 else 1
        if i - row_len >= 0:
            ans[i - row_len] = 0 if ans[i - row_len] == 1 else 1
        if i + row_len < len(vec):
            ans[i + row_len] = 0 if ans[i + row_len] == 1 else 1
        if i % row_len != 0:
            ans[i - 1] = 0 if ans[i - 1] == 1 else 1
        if i % row_len != row_len - 1:
            ans[i + 1] = 0 if ans[i + 1] == 1 else 1
        return ans