# 모든 정점 사이의 최단거리를 구하면 되는 문제
# 거기서 최단거리가 distanceThreshold 아래인 도시들을 구하고, 가장 많이 다른 도시를 갈 수 있는 도시의 인덱스를 리턴하는 문제

class Solution:
    def findTheCity(self, n: int, edges: List[List[int]], distanceThreshold: int) -> int:
        INF = int(1e9)
        graph = [[INF for _ in range(n)] for _ in range(n)]
        
        # 자기 자신에서 자기 자신으로 가는 비용은 0으로 초기화
        for a in range(n):
            for b in range(n):
                if a == b:
                    graph[a][b] = 0
                    graph[b][a] = 0
        
        for edge in edges:
            start, end, weight = edge
            graph[start][end] = weight # 양방향이니까..
            graph[end][start] = weight
        
        # 모든 정점 사이의 최단거리를 구하면 되는 문제 -> 거기에서 최대값을 찾기!
        for k in range(n):
            for a in range(n):
                for b in range(n):
                    graph[a][b] = min(graph[a][b], graph[a][k] + graph[k][b])
        
        res = INF
        res_idx = -1
        for a in range(n):
            cnt = 0
            for b in range(n):
                if graph[a][b] != INF and graph[a][b] <= distanceThreshold:
                    cnt += 1
            if cnt <= res:
                res_idx = a
                res = cnt
                
        return res_idx