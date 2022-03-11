import bisect
class Solution:
    def minAreaRect(self, points: List[List[int]]) -> int:
        x_to_y = collections.defaultdict(list)
        y_to_x = collections.defaultdict(list)
        
        for (x, y) in points:
            x_to_y[x].append(y)
            y_to_x[y].append(x)
            
        for x, y_list in x_to_y.items():
            y_list.sort()
        for y, x_list in y_to_x.items():
            x_list.sort()
         
        points = set([tuple(point) for point in points]) # 이거는 왜 굳이 이렇게 만든느건지 모르겠음.
        smallest = float('inf')

        for x1, y1 in points: 
            y_list = x_to_y[x1] # 현재 x1에서 될수있는 모든 y좌표들
            x_list = y_to_x[y1] # 현재 y1에서 될 수 있는 모든 x좌표들
            
            y_idx = bisect.bisect_right(y_list, y1) # 현재 좌표보다 큰 값들을 찾음
            x_idx = bisect.bisect_right(x_list, x1)
            
            ys_above = y_list[y_idx:]
            xs_right = x_list[x_idx:]
            for x2 in xs_right:
                for y2 in ys_above:
                    if (x2, y2) in points:
                        smallest = min(smallest, (x2 - x1) * (y2 - y1))
                        break
        
        return smallest if smallest != float('inf') else 0