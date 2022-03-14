class Solution:
    def numMatchingSubseq(self, s: str, words: List[str]) -> int:
        
        def isSubsequence(s, word):
            prev_idx = 0
            for i in range(len(word)):
                try:
                    tmp = s.index(word[i], prev_idx)
                    prev_idx = tmp + 1
                except:
                    return False
            return True
            
        res = 0
        for word in words:
            if isSubsequence(s, word):
                res += 1
        return res