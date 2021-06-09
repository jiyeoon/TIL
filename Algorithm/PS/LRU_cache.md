
# 문제 링크

<https://leetcode.com/problems/lru-cache/>

# 문제 풀이

```python
class LRUCache:
    def __init__(self, capacity):
        self.cache = collections.OrderedDict()
        self.capacity = capacity
    
    # key가 있으면 그 키의 값을 리턴. 없으면 -1을 리턴
    def get(self, key):
        if key in self.cache:
            self.cache.move_to_end(key) # 마지막 위치에 사용된 애를 보내버림
            return self.cache[key]
        else:
            return -1
    
    # key가 없으면 key를 업데이트. 
    def put(self, key, value):
        if key in self.cache: # 키가 있으면 키를 업데이트.
            self.cache.pop(key)
        elif len(self.cache) == self.capacity: 
            self.cache.popitem(last=False) # (last=False)라고 주면 처음 값을 리턴하고 삭제.
        
        self.cache[key] = value # 키를 업데이트

```