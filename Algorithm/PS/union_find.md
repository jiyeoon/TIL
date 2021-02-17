# 유니온 파인드

> 유니온 파인드 알고리즘이란?

그래프 알고리즘의 일종. 상호 배타적 집합, Disjoint-set이라고도 한다. 여러 노드가 존재할 때 어떤 두 개의 노드를 같은 집합으로 묶어주고, 다시 어던 두 노드가 같은 집합에 있는지 확인하는 알고리즘. 유니온 파인드는 아래 두가지 연산으로 존재한다.

1. Find
   - 노드 x가 어느 집합에 있는지 찾는 연산
2. Union
   - 노드 x가 포함된 집합과 노드 y가 포함된 집합을 합치는 연산


## 코드 구현

```python
def find(x):
    while self.parent[x] > 0:
        x = self.parent[x]
    return x

def union(x, y):
    root_x = find(x)
    root_y = find(y)

    if root_x == root_y:
        return False
    else:
        self.parent[root_x] = root_y
        return True
```