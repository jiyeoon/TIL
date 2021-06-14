from itertools import permutations
class Solution:
    def nextGreaterElement(self, n: int) -> int:
        s = str(n)
        tmp = [int(''.join(t)) for t in set(permutations(s))]
        tmp.sort()
        idx = tmp.index(n)
        
        try:
            return tmp[idx+1] if tmp[idx+1] <= 2**31 - 1 else -1
        except:
            return -1