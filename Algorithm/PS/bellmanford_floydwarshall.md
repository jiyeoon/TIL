
- [플로이드 와샬 알고리즘 (Floyd Warshall Algorithm)](#플로이드-와샬-알고리즘-floyd-warshall-algorithm)
  - [기본 로직](#기본-로직)
  - [플로이드 와샬 성능 분석](#플로이드-와샬-성능-분석)
  - [코드로 구현하기](#코드로-구현하기)
- [벨만 포드 알고리즘 (Bellman-Ford Algorithm)](#벨만-포드-알고리즘-bellman-ford-algorithm)
  - [동작 원리](#동작-원리)
  - [벨만포드의 슈도코드](#벨만포드의-슈도코드)
  - [벨만포드의 성능](#벨만포드의-성능)
  - [샘플 코드](#샘플-코드)

> 최단 경로 알고리즘의 종류

1. 다익스트라 알고리즘 (Dijkstra's Algorithm)
   - 가장 유명한 알고리즘. 단일 정점의 최단 경로를 구할 수 있다.
2. 벨만 포드 알고리즘 (Bellman-Ford Algoirthm)
   - 음의 가중치를 가진 경로에서도 최단거리를 구할 수 있다. 
   - 경로 추적이 가능하다.
3. 플로이드 와샬 알고리즘 (Floyd-Warshall Algorithm)
   - 단일 정점이 아닌 모든 정점 사이의 최단 거리를 구할 수 있다.
4. SPFA (Shortest Path Faster Algorithm)
   - STL 없이 간단하게 구현 가능하며, 평균적으로 빠른 속도를 가진다.


# 플로이드 와샬 알고리즘 (Floyd Warshall Algorithm)

다익스트라는 하나의 정점에서 출발했을 때 다른 모든 정점으로의 최단 경로를 구하는 알고리즘이라면, 플로이드 와샬 알고리즘은 <u>'모든 정점'에서 '모든 정점'으로의 최단 경로</u>를 구하는 알고리즘입니다. 

다익스트라 알고리즘은 가장 적은 비용을 하나씩 선택했다면 플로이드 와샬 알고리즘은 기본적으로 **거쳐가는 정점**을 기준으로 알고리즘을 수행한다는 점에서 그 특징이 있습니다. 

다익스트라와 마찬가지로 플로이드 와샬 또한 기본적으로 다이나믹 프로그래밍 기술에 의거합니다. 

## 기본 로직

플로이드 와샬에서는 2개의 테이블을 사용합니다.

1. 모든 경로에 대한 비용을 저장하는 테이블 (=D)
2. 각 정점까지 가기 직전의 정점을 저장한 테이블 (=P)

각각의 테이블을 D와 P라고 했을 때, 테이블 D와 P에는 처음엔 인접 리스트에 대한 내용들만 들어가게 됩니다. 그 후 경로를 추가할 때 마다 두 테이블이 갱신됩니다.

- **초기 상태** : 그래프를 준비하고 최단거리 테이블을 초기화한다.
  - ![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fc0b3mJ%2FbtqSmzRxbKw%2FAFr6HNli1JPcRkicbZ8uM0%2Fimg.png)
- **Step 1** : 1번 노드를 거쳐가는 경우를 고려하여 테이블을 갱신한다.
  - ![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FpGzgI%2FbtqSpGpfTGj%2F9M53sB6KMk5Tdio0Aryxmk%2Fimg.png)
- **Step 2** : 2번 노드를 거쳐가는 경우를 고려하여 테이블을 갱신한다.
  - ![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbO0GVm%2FbtqSsQSEsmc%2FFsgbpWf2y2RgtrspEAQkN0%2Fimg.png)
- **Step 3** : 3번노드,, 4번노드 계속해서 반복한다. 
  - ![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FOgWop%2FbtqSEKcIr8X%2FzW44u4yRK0JimbeDub1N70%2Fimg.png)
  - ![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2F7Lyb9%2FbtqSgLZbDeP%2FAfiK6gyoNAwdZ6s4wEqSKk%2Fimg.png)

각 단계마다 특정 노드 k를 거쳐가는 경우를 확인하는 것이 핵심입니다. 즉, a에서 b로가는 최단거리보다 a에서 k를 거쳐 b로가는 거리가 더 짧은지 검사해야합니다. 

점화식은 아래와 같습니다.

![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FczGTrB%2FbtqSDtI4Is2%2Fyv1uv6MOkJgWVbMyPAcx90%2Fimg.png)

## 플로이드 와샬 성능 분석

- 노드의 개수가 N개일 때 알고리즘 상으로 N번의 단계를 수행합니다.
  - 각 단계마다 $O(N^2)$의 연산을 통해 현재 노드를 거쳐가는 모든 경로를 고려한다.
- 따라서 플로이드 와샬 알고리즘의 시간 복잡도는 $O(N^3)$이다.


## 코드로 구현하기

```python
INF = int(1e9) # 무한을 의미하는 값으로 10억 설정

# 노드의 개수 및 간선의 개수 입력받기
n, m = map(int, input().split())
# 2차원 리스트(그래프 표현)를 만들고 모든 값을 무한으로 초기화
graph = [[INF] * (n+1) for _ in range(n+1)]

# 자기 자신에서 자기 자신으로 가는 비용은 0으로 초기화
for a in range(1, n+1):
    for b in range(1, n+1):
        if a == b:
            graph[a][b] = 0

# 각 간선에 대한 정보를 입력받아 그 값으로 초기화
for _ in range(m):
    a, b, c = map(int, input().split())
    graph[a][b] = c

# 점화식에 따라 플로이드 와샬 알고리즘을 수행
for k in range(1, n+1):
    for a in range(1, n+1):
        for b in range(1, n+1):
            graph[a][b] = min(graph[a][b], graph[a][k] + graph[k][b])

# 수행된 결과를 출력
for a in range(1, n+1):
    for b in range(1, n+1):
        # 도달할 수 없는 경우 무한이라고 출력
        if graph[a][b] == INF:
            print("INF", end=" ")
        else:
            print(graph[a][b], end=" ")
    print()
```

---

# 벨만 포드 알고리즘 (Bellman-Ford Algorithm)

벨만포드에서는 **음의 가중치**를 갖는 그래프에서 최단경로를 찾는 것이 목적입니다. 

## 동작 원리

벨만포드 알고리즘을 통해 최단거리를 구하는 방식은 계속해서 모든 간선을 이용하여 a정점에서 b정점으로 갈 때 거리가 짧아지는 경우가 생긴다면 계속 업데이트를 해주는 방식이다. V(정점) x E(간선)번 반복 후 종료한다.

![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Ft1.daumcdn.net%2Fcfile%2Ftistory%2F992A1E4D5E171A1D08)

![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Ft1.daumcdn.net%2Fcfile%2Ftistory%2F992A1E4D5E171A1D08)

![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Ft1.daumcdn.net%2Fcfile%2Ftistory%2F99FFE04C5E171A263A)

![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Ft1.daumcdn.net%2Fcfile%2Ftistory%2F991DF44D5E171A3033)


## 벨만포드의 슈도코드

![img](https://i.imgur.com/Co6NVQ8.png)



## 벨만포드의 성능

벨만포드 알고리즘은 그래프의 모든 엣지에 대해 edge relaxation을 시작노드를 제외한 전체 노드수 만큼 반복 수행하고, 마지막으로 그래프의 모든 엣지에 대해 edge relaxtion을 1번 수행해주므로 그 계산 복잡성은 $O(|V||E|)$이 됩니다. 그런데 dense graph는 엣지 수가 대개 노드 수의 제곱에 근사하므로 간단하게 표현하면 $O({|V|}^3)$이 됩니다. 이는 다익스트라 알고리즘보다 더 큽니다. 음수 가중치가 있을 경우에만 벨만 포드를 사용해주는 것이 좋겠습니다!

## 샘플 코드

```python
# Bellman-Ford implementation from MIT 6006 course lesson #17
import math
import networkx as nx

# utility: Graph
class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.edges = []
    
    def add_edge(self, edge):
        self.edges.append(edge)
        
    def __str__(self):
        result = ''
        for edge in self.edges:
            result += f'{v}: {str(edge)}, \n'
        return result

def bellmanFord(graph, s):
    """
    Idea behind bellman-ford vs dijkstra:
    
    They both can be used to find shortest path. But their approach is different.

    Dijkstra is a greedy algorithm, which means it makes 'best optimal answer' for each given step.
    But it fails when it encounters negative weights. Why? Because you can improve the weight by adding
    one more iteration of relaxing all the edges.

    However, Bellman-Ford is not a greedy algorithm. It just inspects for all the possible improvements
    simply by looping over edges |V| - 1 times to get the best weight for 'shortest simple path'(SSP).
    Then why |V| - 1 times? The length of the longest simple path(path w/o cycle) would be |V| - 1.
    For example, you need 2 edges to connect 3 vertices, otherwise, there exists a negative cycle.
    """
    d = dict.fromkeys(graph.V, math.inf) # distance pair 
                                         # will have default value of Infinity
    pi = dict.fromkeys(graph.V, None) # map of parent vertex
    
    # initialize
    d[s] = 0
    
    def relax(u, v, w):
        if d[v] > d[u] + w:
            d[v] = d[u] + w
            pi[v] = u
    
    # The length of the longest simple path(path w/o cycle) would be |V| - 1.
    # For example, you need 2 edges to connect 3 vertices.
    # Otherwise, there exists a negative cycle.
    for i in graph.V[:-1]:
        for u, v, w in graph.edges:
            relax(u, v, w)
            
    for u, v, w in graph.edges:
        # even after relaxing all the edges for |V| - 1 times,
        # we still have the posibillity to improve the existing path
        # this means there are negative cycles
        if d[v] > d[u] + w:
            return f'there exists a negetive cycle!'
                
    return d, pi

def shortest_path(s, t):
    try:
        d, pi = bellmanFord(g, s)
    except ValueError:
        return 'you can\'t find shortest path if the graph has negative cycle!'
    
    path = [t]
    current = t
    
    # if parent pointer is None,
    # then it's the source vertex
    while pi[current]:
        path.insert(0, pi[current])
        # set current to parent
        current = pi[current]
    
    if s not in path:
        return f'unable to find shortest path staring from "{s}" to "{t}"'
    
    return f'{" > ".join(path)}'

g = Graph(['A', 'B', 'C', 'D', 'E'])

# graph with negative cycle
nc_edges = [('A', 'B', 5), ('B', 'C', -1), ('C', 'D', 2), ('D', 'B', -2), ('C', 'E', 4)]

# w/o negative cycles
edges = [\
    ('A', 'B', 10), ('A', 'C', 3), ('B', 'C', 1), ('C', 'B', 4), \
    ('B', 'D', 2), ('C', 'D', 8), ('D', 'E', 7), ('E', 'D', 9), ('C', 'E', 2)]

# used for both finding shortest path and drawing graph
current_edge_group = edges

for edge in current_edge_group:
    g.add_edge(edge)

print( shortest_path('A', 'E') )

G = nx.DiGraph()
G.add_weighted_edges_from(current_edge_group)
nx.draw(G, with_labels = True, node_color='b', font_color='w')
```