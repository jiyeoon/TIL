class RangeModule:

    def __init__(self):
        self.ranges = []

    def touching_ranges(self, left, right):
        '''find all the ranges that touch interval [left, right]'''
        i, j = 0, len(self.ranges)-1
        step = len(self.ranges) // 2
        while step >= 1:
            while i + step < len(self.ranges) and self.ranges[i+step-1][1] < left:
                i += step
            while j - step >= 0 and self.ranges[j-step+1][0] > right:
                j -= step
            step //= 2
        return i, j
        
    def addRange(self, left: int, right: int) -> None:
        if not self.ranges or self.ranges[-1][1] < left: 
            self.ranges.append((left, right))
            return
        if self.ranges[0][0] > right:
            self.ranges.insert(0, (left, right))
            return
        i, j = self.touching_ranges(left, right)
        self.ranges[i:j+1] = [(min(self.ranges[i][0], left), max(self.ranges[j][1], right))]
        
    def queryRange(self, left: int, right: int) -> bool:
        if not self.ranges: return False
        i, j = self.touching_ranges(left, right)
        return self.ranges[i][0] <= left and right <= self.ranges[i][1]

    def removeRange(self, left: int, right: int) -> None:
        if not self.ranges or self.ranges[0][0] > right or self.ranges[-1][1] < left: return
        i, j = self.touching_ranges(left, right)
        new_ranges = []
        for k in range(i, j+1):
            if self.ranges[k][0] < left:
                new_ranges.append((self.ranges[k][0], left))
            if self.ranges[k][1] > right:
                new_ranges.append((right, self.ranges[k][1]))
        self.ranges[i:j+1] = new_ranges