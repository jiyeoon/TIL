# 유니온 파인드

> 유니온 파인드 알고리즘이란?

그래프 알고리즘의 일종. 상호 배타적 집합, Disjoint-set이라고도 한다. 여러 노드가 존재할 때 어떤 두 개의 노드를 같은 집합으로 묶어주고, 다시 어던 두 노드가 같은 집합에 있는지 확인하는 알고리즘. 

표현하려는 집합들은 어떤 두 집합 사이에도 교집합의 원소가 하나도 없고, 모든 집합의 합집합은 전체집합이라는 의미다. 이 자료구조는 항상 여러 개의 트리 형태를 띄고 있으며, 그 트리 컴포넌트들이 각각 하나의 집합이다.

유니온 파인드는 아래 두가지 연산으로 존재한다.

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

### 1. Find 연산

두 원소가 같은 집합에 속해있는지 확인하는 방법. 각각의 루트(root)를 찾아서 둘이 같은지 비교하는 것. 

![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=http%3A%2F%2Fcfile24.uf.tistory.com%2Fimage%2F2776E14858D2A551210DDE)

위와 같이 u가 있고 find(u)를 실행하면 `u!=parent[u]`이기 때문에 계속해서 부모 노드를 착데 된다. u의 부모인 한칸 위의 노드로 향하게 된다.

![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=http%3A%2F%2Fcfile29.uf.tistory.com%2Fimage%2F26394D4858D2A55225074A)

여기서도 마찬가지로 부모 노드가 아니기 때문에 한칸 더 위로 올라간다.

![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=http%3A%2F%2Fcfile30.uf.tistory.com%2Fimage%2F247F394858D2A55207926C)

가장 위의 노드가 부모 노드이기 때문에 `u==parent[u]`를 만족하게 된다. 따라서 여기를 리턴한다.


### 2. Union 연산

u의 노드가 있는 트리와 v의 노드가 있는 트리를 합친다고 생각해보자. 

![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=http%3A%2F%2Fcfile23.uf.tistory.com%2Fimage%2F22363B4D58D2A7661A7564)

위의 Find 연산을 통해서 u가 들어있는 루트 노드인 r1, v가 들어있는 루트 노드인 r2를 알 수 있게 된다.

`u = Find(u)`, `v = Find(v)` 연산을 했을 때 `u==v`라면 그대로 종료를 하면 되지만, 위 사진의 경우 그렇지 않은 경우이기 때문에 Union 연산을 해준다. 

![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=http%3A%2F%2Fcfile30.uf.tistory.com%2Fimage%2F213FB14A58D2AAC0120362)

`self.parent[root_x] = root_y` 로, v의 루트 노드를 u의 루트노드 밑에 넣어준다. 두 트리를 하나로 묶어주는 과정이다.

만약 두 트리가 같은 레벨의 트리였다면 루트 노드가 있는 level 배열을 1 늘려주면 된다. 



## 시간 복잡도

유니온 파인드 자료구조는 매우 간단하면서도 좋은 효율을 자랑한다.

1. Find 연산의 시간복잡도
   - $O(\log N)$
2. Union 연산의 시간 복잡도
   - $O(\log N)$




---

> Reference

- [corocus님의 유니온 파인드(Union Find, Disjoint Set)](https://www.crocus.co.kr/683)
