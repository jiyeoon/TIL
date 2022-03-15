class Solution:
    def getOrder(self, tasks: List[List[int]]) -> List[int]:
        heap = []
        available = []
        for i, (e, p) in enumerate(tasks):            
            heappush(heap, (e, p, i))

				e, p, i = heappop(heap)
        last = e + p
        res = [i]        
        while heap or available:            
            while heap and heap[0][0] <= last:
                e, p, i = heappop(heap)
                heappush(available, (p, i, e))
                
            if not available:
                e, p, i = heappop(heap)
                heappush(available, (p, i, e))
                
            p, i, e = heappop(available)
            res.append(i)
            last = max(p + e, last + p)
            
        return res