import math
import bisect

class Solution:
    def visiblePoints(self, points: List[List[int]], angle: int, location: List[int]) -> int:
        pos_x, pos_y = location
        points = [(x - pos_x, y - pos_y) for x, y in points]
        
        base_cnt = 0
        theta = []
        for x, y in points:
            if x == 0 and y > 0:
                theta.append(math.radians(90))
            elif x == 0 and y < 0:
                theta.append(math.radians(270))
            elif x == 0 and y == 0:
                base_cnt += 1
            else:
                y_x = abs(y/x)
                if x > 0 and y >= 0:
                    theta.append(math.atan(y_x))
                elif x > 0 and y < 0:
                    theta.append(math.radians(360) - math.atan(y_x))
                elif x < 0 and y >= 0:
                    theta.append(math.radians(180) - math.atan(y_x))
                elif x < 0 and y < 0:
                    theta.append(math.radians(180) + math.atan(y_x))
                    
        if not theta:
            return base_cnt
        
        theta.sort()
        res = -float('inf')
        
        for t in theta:
            start_angle, end_angle = t, t + math.radians(angle)
            start_angle = start_angle if start_angle <= math.radians(360) else start_angle - math.raians(360)
            end_angle = end_angle if end_angle <= math.radians(360) else end_angle - math.radians(360)
            degree_range = (start_angle, end_angle)
            cnt = 0
            
            if degree_range[0] <= degree_range[1]: # 아... 이건 전부 이렇게 되지..... 당연......
                left_idx = bisect.bisect_left(theta, degree_range[0])
                right_idx = bisect.bisect_right(theta, degree_range[1])
                cnt = (right_idx - left_idx)
            else:
                left_idx = bisect.bisect_right(theta, degree_range[1])
                right_idx = bisect.bisect_left(theta, degree_range[0])
                cnt = left_idx + (len(theta) - right_idx)
            res = max(res, cnt + base_cnt)
        return res