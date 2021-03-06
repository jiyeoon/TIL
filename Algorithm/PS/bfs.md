
# DFS와 BFS

![img](https://ww.namu.la/s/1fe9246903b78fae07577b243a0b22791e02cb39640d5cbaae10d9849343b4ea6f162a9a677a5892fbf7819abd4ef7221ebd3608849cfb66793411fb5e643951c59adc4f1cfbe5b5a869e338dc7576bc940ae87fbdf8b769c5478c0246aca29a)


> 시작하기 전에... 그래프의 표현 방법

#### 1. 인접 행렬(Adjacency Matrix)

2차원 배열로 그래프의 연결관계를 표현하는 방식

```python
INF = 99999999999999
graph = [
    [0, 7, 5],
    [7, 0, INF],
    [5, INF, 0]
]
```

#### 2. 인접 리스트(Adjacency List)

리스트로 그래프의 연결 관계를 표현하는 방식

```python
graph = [[] for _ in range(3)]
graph[0].append((1, 7)) # 0번 노드는 1번 노드와 7의 거리로 연결되어 있다는 뜻
```

## 여러가지 트리 순회 알고리즘

![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbIDSTw%2Fbtq3hnrPpgQ%2FjGpx6PvM60CtpKO23NeI21%2Fimg.png)

1. 전위 순회 (preorder)
    - 현재 노드 -> 왼쪽 트리 -> 오른쪽 트리 순서대로 방문하는 방법.
2. 중위 순회 (Inorder)
    - 왼쪽 트리 -> 현재 노드 -> 오른쪽 트리 순서대로 방문하는 방법
3. 후위 순회 (Postorder)
    - 왼쪽 트리 -> 오른쪽 트리 -> 현재 노드 순서대로 방문하는 방법
4. 레벨 순서 순회 (level-order)
    - 모든 노드를 낮은 레벨부터 차례대로 순회. (=BFS)


## BFS 

Breadth First Search, 줄여서 BFS라고 합니다. 흔히 "너비우선탐색"이라고 부릅니다.

**가까운 노드부터** 탐색하는 알고리즘으로, DFS는 깊이를 우선적으로 탐색했다면 BFS는 그 반대입니다. 

BFS에서는 선입선출 방식인 **큐** 자료구조를 사용하는 것이 정석으로, 인접한 노드를 반복적으로 큐에 넣도록 알고리즘을 작성하면 자연스럽게 먼저 들어온 것이 먼저 나가게 되어 가까운 노드부터 탐색을 진행할 수 있습니다.


### 알고리즘 동작 방식

1. 탐색 시작 노드를 큐에 삽입하고 방문 처리를 한다.
2. 큐에서 노드를 꺼내 해당 노드의인접 노드 중에서 방문하지 않은 노드를 모두 큐에 삽입하고 방문 처리를 한다.
3. 2번의 과정을 더이상 수행할 수 없을 때까지 반복한다. 


### 특징

한 갈림길에서 연결되는 모든 길을 한번씩 탐색하기 때문에 *가중치가 없는 그래프*에서는 시작점에서 끝점까지의 최단경로를 알아낼 수 있다. 


### 샘플 코드

BFS는 큐 자료구조에 기초한다는 점에서 구현이 간단하다. 파이썬에서는 `deque` 라이브러리를 사용하는 것이 좋으며 탐색을 수행하는데에 있어 $O(N)$의 사긴아 소요된다. 일반적인 경우 실제 수행 시간은 DFS보다 좋은 편이다. 

```python
from collections import deque

def bfs(graph, start, visited):
    queue = deque([start])
    visited[start] = True
    while queue:
        v = queue.popleft()
        for i in graph[v]:
            if not visitied[i]:
                queue.append(i)
                visitied[i] = True
```

## DFS

Depth First Search, 줄여서 DFS라고 쓴다. 

트리나 그래프에서 한 루트로 계속 탐색하다가 다시 돌아돠 다른 루트로 탐색하는 방식이다. 대표적으로 *백트레킹*에 사용한다. 일반적으로 **재귀호출**을 사용하여 구현하기도 하지만 단순한 스택 배열로 구현하기도 한다. 구조상 스택 오버플로우를 주의해야 한다.

단순 검색 속도 자체는 BFS에 비해 느리다. 하지만 검색이 아닌 트래버스(traverse)를 할 경우는 많이 쓰인다. DFS는 특히 리프 노드에만 데이터를 저장하는 정렬 트리 구조에서 항상 순서대로 데이터를 방문한다는 장점이 있다. 


### 동작 과정

#### 스택 자료구조를 사용하는 방법

1. 탐색 시작 노드를 스택에 삽입하고 방문 처리를 한다.
2. 스택의 최상단 노드에 방문하지 않은 인접 노드가 있으면 그 인접 노드를 스택에 넣고 방문 처리를 한다. 방문하지 않은 인접 노드가 없으면 스택에서 최상단 노드를 꺼낸다.
3. 2번의 과정을 더이상 수행할 수 없을 때까지 반복한다. 

### 장단점

- 장점
  - 단지 현 경로상의 노드들만 기억하면 되므로 저장 공간의 수요가 비교적 작다.
  - 목표 노드가 깊은 단계에 있을 경우 해를 빨리 구할 수 있다.
- 단점
  - 해가 없는 경로에 깊이 빠질 가능성이 있다.
  - 얻어진 해가 최단 경로가 된다는 보장이 없다. 

### 예제 코드

```python
def dfs(graph, v, visited):
    visited[v] = True
    for i in graph[v]:
        if not visited[i]:
            dfs(graph, i, visited)
```