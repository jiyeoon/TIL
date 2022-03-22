class Solution:
    def checkRecord(self, n: int) -> int:
    	C, m = [1,1,0,1,0,0], 10**9 + 7
    	for i in range(n-1):
    		a, b = sum(C[:3]) % m, sum(C[3:]) % m
    		C = [a, C[0], C[1], a + b, C[3], C[4]]
    	return (sum(C) % m)