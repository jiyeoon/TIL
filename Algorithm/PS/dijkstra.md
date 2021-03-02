- [다익스트라 최단경로 알고리즘](#다익스트라-최단경로-알고리즘)
  - [다익스트라 최단경로 알고리즘이란?](#다익스트라-최단경로-알고리즘이란)
  - [동작 원리](#동작-원리)
  - [구현하기](#구현하기)
    - [방법 1. 간단한 다익스트라 알고리즘](#방법-1-간단한-다익스트라-알고리즘)
    - [방법 2. 개선된 다익스트라 알고리즘](#방법-2-개선된-다익스트라-알고리즘)

# 다익스트라 최단경로 알고리즘

> 최단 경로 (shortest path) 알고리즘이란?

말 그대로 가장 짧은 경로를 찾는 알고리즘. 최단 경로 알고리즘 유형에는 다양한 종류가 있는데, 상황에 맞는 호율적인 알고리즘이 이미 정립되어 있다.

최단 경로 알고리즘은 보통 그래프로 표현하는데 각 지점은 그래프에서 '노드'로 표현되고, 지점간 연결ㄷ죈 도로는 그래프에서 '간선'으로 표현된다. 

컴퓨터공학과 학부 수준에서 사용하는 최단거리 알고리즘은 

1. 다익스트라 최단경로 알고리즘
2. 플로이드 워셜
3. 벨만포드 알고리즘

이렇게 세가지다. 그리디 알고리즘과 다이나믹 프로그래밍 알고리즘이 최단경로 알고리즘에 그대로 적용되어 그리디 및 dp의 한 유형으로 볼 수 있다.

## 다익스트라 최단경로 알고리즘이란?

그래프에서 여러개의 노드가 있을 때, 특정 노드에서 출발하여 다른 노드로 가는 각각의 최단 경로를 구해주는 알고리즘.

'음의 간선'이 없을 때 정상적으로 동작하며, 현실세계에서 GPS 소프트웨어의 기본 알고리즘으로 채택되곤 한다. 

기본적으로 그리디 알고리즘으로 분류되는데, 매번 '가장 비용이 적은 노드'를 선택하여 임의의 과정을 반복하는 식으로 구성된다. 알고리즘의 원리는 아래와 같다.

1. 출발 노드를 설정한다.
2. 최단거리 테이블을 초기화한다
3. 방문하지 않은 노드 중에서 최단거리가 가장 짧은 노드를 선택한다.
4. 해당 노드를 거쳐 다른 노드로 가는 비용을 계산하여 최단거리 테이블을 갱신한다.
5. 위 과정에서 (3)과 (4)를 반복한다.

다익스트라 알고리즘은 최단 경로를 구하는 과정에서 *각 노드에 대한 현재까지의 최단 거리* 정보를 항상 1차원 리스트에 저장하며 리스트를 계속 생신한다는 특징이 있다. 매번 현재 처리하고 있는 노드를 기준으로 주변 간선을 확인한다. 나중에 현재 처리하고 있는 노드와 인접한 노드로 도달하는 더 짧은 경로를 찾으면 해당 경로를 짧은 경로로 판단한다. 따라서 *방문하지 않은 노드 중에서 현재 최단거리가 가장 짧은 노드를 확인*헤 그 노드에 대하여 4번 과정을 수행한다는 점에서 그리디 알고리즘으로 볼 수 있다. 


## 동작 원리

아래와 같이 그래프가 있을 때, 1번 노드에서 다른 노드로 가는 최단경로를 구하는 문제를 생각해보자. 

- [Step 0] 초기 상태
   - ![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2Fqopgr%2FbtqKC9EAKzQ%2FT75o2FzTptAlRxeZQg47c1%2Fimg.png)
   - 초기 상태에서는 다른 노드로 가는 최단 거리를 '무한'으로 초기화한다.
- [Step 1] 1번 노드를 처리한다.
  - ![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FTY66Q%2FbtqKAAiomTC%2FA7RMZ7qDmyzlP8Knu1cV41%2Fimg.png)
  - 1번 노드와 연결된 모든 간선을 하나씩 확인한다. 1번 노드를 거쳐서 2번, 3번, 4번 노드로 가는 최소 비용을 차례로 더해서 구해준다. 기존에는 2번, 3번, 4번 노드가 '무한'으로 설정되어있었는데 새 노드에 대해 더 짧은 경로를 찾았으므로 새로운 값으로 갱신해준다. 
- [Step 2] 방문하지 않은 노드 중에서 최단 거리가 가장 짧은 노드인 4번을 처리한다.
  - ![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2F6I2H2%2FbtqKAAionqO%2FnKdK0wLSRXO9GDweEHkzB1%2Fimg.png)
  - 4번 노드에서 4번 노드를 거쳐서 갈 수 있는 노드를 확인한다. 4번 노드에서 갈 수 있는 노드는 3번과 5번으로, 4번까지의 최단거리가 1이므로 4번 노드를 거쳐서 3번과 5번 노드로 가는 비용을 새로 계산해준다. 기존 리스트에 담겨있는 값보다 작으므로 리스트가 갱신된다.
- 모든 노드를 방문할 때 까지 반복한다.


## 구현하기

다익스트라 알고리즘을 구현하는 방법은 2가지이다. 하나는 구현하기 쉽지만 느리게 동작하는 코드, 다른 하나는 구현하기에  조금 더 까다롭지만 빠르게 동작하는 코드이다. 

### 방법 1. 간단한 다익스트라 알고리즘

간단한 다익스트라 알고리즘은 $O(V^2)$의 시간복잡도를 가지며, 다익스트라에 의해서 처음 고안되었던 알고리즘이다. 여기서 V는 노드의 개수를 의미한다. 

처음에 각 노드에 대한 최단거리를 담는 1차원 리스트를 선언하고, 이후 단계마다 '방문하지 않은 노드 중에서 최단 거리가 가장 짧은 노드를 선택'하기위해 매 단계마다 1차원리스트이 모든 원소를 순차 탐색 한다.

```python
import sys
input = sys.stdin.readline
INF = int(1e9) # 무한을 의미하는 값으로 10억을 설정

# 노드의 개수, 간선의 개수를 입력받기
n, m = map(int, input().split())
# 시작 노드 번호를 입력받기
start = int(input())
# 각 노드에 연결되어있는 노드에 대한 정보를 담는 리스트 만들기
graph = [[] for _ in range(n+1)]
# 방문한적이 있는지 체크하는 리스트 만들기
visited = [False] * (n+1)
# 최단거리 테이블을 모두 무한으로 초기화
distance = [INF] * (n+1)

# 모든 간선 정보를 입력받기
for _ in range(m):
    a, b, c = map(int, input().split())
    # a번 노드에서 b번 노드로 가는 비용이 c라는 의미
    graph[a].append((b, c))

# 방문하지 않은 노드 중에서 가장 최단거리가 짧은 노드의  번호를 반환
def get_smallest_node():
    min_value = INF
    index = 0
    for i in range(1, n+1):
        if distance[i] < min_value and not visited[i]:
            min_value = distance[i]
            index = i
    return index

def dijkstra(start):
    # 시작 노드에 대해서 초기화
    distance[start] = 0
    visited[start] = True
    for j in graph[start]:
        distance[j[0]] = j[1]
    for i in range(n-1):
        # 현재 최단거리가 가장 짧은 노드를 꺼내서 방문 처리
        now = get_smallest_node()
        visited[now] = True
        # 현재 노드와 연결된 다른 노드를 확인
        for j in graph[now]:
            cost = distance[now] + j[1]
            # 현재 노드를 거쳐서 다른 노드로 이동하는 거리가 더 짧은 경우
            if cost < distance[j[0]]:
                distance[j[0]] = cost

dijkstra(start)

# 몯즌 노드로 가기 위한 최단 거리를 출력
for i in range(1, n+1):
    if distance[i] == INF:
        print("Infinity")
    else:
        print(distance[i])
```

시간 복잡도는 $O(V^2)$인데, 왜냐하면 총 $O(V)$번에 걸쳐서 최단거리가 가장 짧은 노드를 매번 선형탐색해야 하고, 현재 노드와 연결된 노드를 매번 일일이 확인하기 때문이다.

따라서 코딩 테스트의 최단 경로 문제에서 전체 노드의 개수가 5000개 이하라면 일반적으로 이 코드로 문제를 풀 수 있을 것이다. 


### 방법 2. 개선된 다익스트라 알고리즘

노드의 개수가 10,000개를 넘어가는 문제라면 이 코드로는 문제를 해결하기가 어렵다. 노드의 개수 및 간선의 개수가 많을 때는 '개선된 다익스트라 알고리즘'을 사용하는 것이 좋다.

이 방법을 사용하면 최악의 경우에도 시간복잡도 $O(E\log V)$를 보장하여 해결할 수 있다. 여기서 V는 노드의 개수이고, E는 간선의 개수이다.

개선된 다익스트라 알고리즘에서는 힙(heap) 자료구조를 사용한다. 힙 자료구조를 이용하게되면 특정 노드까지의 최단거리에 대한 정보를 힙에 담아서 처리하므로 출발 노드로부터 가장 거리가 짧은 노드를 더욱 빠르게 찾을 수 있다. 


```python
import heapq
import sys
input = sys.stdin.readline
INF = int(1e9)

# 노드의 개수, 간선의 개수 입력받기
n, m = map(int, input().split())
# 시작 노드 번호 입력받기
start = int(input())
# 각 노드에 연결되어있는 노드에 대한 정보를 담는 리스트를 만들기
graph = [[] for i in range(n+1)]
# 최단거리 테이블을 모두 무한으로 초기화
distance = [INF] * (n+1)

# 모든 간선 정보 입력받기
for _ in range(m):
    a, b, c = map(int, input().split())
    graph[a].append((b, c))

def dijkstra(start):
    q = []
    # 시작 노드로 가기위한 최단 경로는 0으로 설정하여 큐에 삽입
    heapq.heappush(q, (0, start))
    distance[start] = 0
    while q: # 큐가 비어있지 않다면
        # 가장 최단거리가 짧은 노드에 대한 정보 꺼내기
        dist, now = heapq.heappop(q)
        # 현재 노드가 이미 처리된 적이 있는 노드라면 무시
        if distance[now] < dist:
            continue
        # 현재 노드와 연결된 다른 인접한 노드들을 확인
        for i in graph[now]:
            cost = dist + i[1]
            # 현재 노드를 거쳐서 다른 노드로 이동하는 거리가 더 짧은 경우
            if cost < distance[i[0]]:
                distance[i[0]] = cost
                heapq.heappush(q, (cost, i[0]))

dijkstra(start)

# 출력
for i in range(1, n+1):
    if distance[i] == INF:
        print("Infinity")
    else:
        print(distance[i])

```

---

> Reference

- <https://freedeveloper.tistory.com/277>