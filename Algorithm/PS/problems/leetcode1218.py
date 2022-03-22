class Solution:
    def longestSubsequence(self, arr: List[int], difference: int) -> int:
        """
        dp is a hashtable, dp[x] is the longest subsequence ending with number x
        """
        dp = {}
        for x in arr:
            if x - difference in dp:
                dp[x] = dp[x-difference] + 1
            else:
                dp[x] = 1
            
        return max(dp.values())