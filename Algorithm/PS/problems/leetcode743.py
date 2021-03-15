from collections import defaultdict

INF = int(1e9)
class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        visited = [0 for _ in range(n+1)]
        distance = [INF for _ in range(n+1)]
        graph = defaultdict(list)
        
        for time in times:
            start, end, cost = time
            graph[start].append([end, cost])
        
        print(graph)
        
        def get_smallest_node():
            nonlocal visited, distance, graph
            min_value = INF
            index = 0
            for i in range(1, n+1):
                if distance[i] < min_value and not visited[i]:
                    min_value = distance[i]
                    index = i
            return index
        
        def dijkstra(start):
            nonlocal visited, distance, graph
            visited[start] = 1
            distance[start] = 0
            for j in graph[start]:
                distance[j[0]] = j[1]
            for i in range(n-1):
                now = get_smallest_node()
                visited[now] = 1
                for j in graph[now]:
                    cost = distance[now] + j[1]
                    if cost < distance[j[0]]:
                        distance[j[0]] = cost
        
        dijkstra(k)
        print(distance)
        if INF not in distance[1:]:
            return max(distance[1:])
        else:
            return -1
        