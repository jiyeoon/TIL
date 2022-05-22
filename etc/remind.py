# example
# words = ['a', 'aa', 'ab', 'ba', 'baa', 'bab', 'bax', 'cax']
# prefix = 'ba'
# return 4

# O(N) Solution
def solution(words, prefix):
    res = 0
    for word in words: # O(N)
        if word.startswith(prefix): # O(1)
            res += 1
    return res

def startswith(word, prefix):
    return True if word[:len(prefix)] == prefix else False


# O (log N) Solution
def solution(words, prefix):
    def bisect_left(words, prefix):
        left, right = 0, len(words)-1
        mid = (left + right) // 2
        res = float('inf')
        
        while left < right:
            mid = (left + right) // 2
            curr = words[mid]
            
            if curr.startswith(prefix):
                res = min(res, mid)
                mid = right - 1
            elif curr > prefix:
                right = mid - 1
            elif curr < prefix:
                left = mid + 1
        
        return res
    
    def bisect_right(words, prefix):
        left, right = 0, len(words)-1
        mid = (left + right) // 2
        res = -1
        
        while left < right:
            mid = (left + right) // 2
            curr = words[mid]
            
            if curr.startswith(prefix):
                res = max(res, mid)
                mid = left + 1
            elif curr > prefix:
                right = mid - 1
            elif curr < prefix:
                left = mid + 1
        
        return res
    
    start, end = bisect_left(words, prefix), bisect_right(words, prefix)
    if start == float('inf') or end == -1:
        return 0
    return start - end + 1




