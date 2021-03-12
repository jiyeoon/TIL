# BOJ 11657 타임머신
INF = int(1e9)
n, m = map(int, input().split())
graph = [[] for _ in range(n+1)]
for _ in range(m):
    start, end, cost = map(int, input().split())
    graph[start].append([cost, end])
distance = [INF] * (n+1)
distance[1] = 0

def bellmanford():
    isPossible = True
    
    for repeat in range(n):
        for i in range(1, n+1):
            for wei, vec in graph[i]:
                if distance[i] != INF and distance[vec] > distance[i] + wei:
                    distance[vec] = distance[i] + wei
                    if repeat == n-1:
                        isPossible = False
    
    return isPossible

res = bellmanford()
if res:
    for d in distance[2:]:
        print(d if d != INF else -1)
else:
    print(-1)