import argparse
from sol import solution
import logging

logger = logging.getLogger('my')
logger.setLevel(logging.INFO)

def solution(D, I, S, V, F, adj, roadnm_to_path, path_to_roadnm, car):
    res = []
    num_intersection = 0
    for _to in range(I+1):
        cnt = 0
        tmp = []
        for _from in range(I+1):
            if adj[_from][_to] != 0:
                road_nm = path_to_roadnm['[{}, {}]'.format(_from, _to)]
                tmp.append(road_nm)
                cnt += 1
        if cnt == 0:
            continue
        res.append([_to])
        res.append([cnt])
        for i in range(cnt):
            res.append([tmp[i], 1])
        num_intersection += 1

        if _to % 1000 == 0:
            logger.info('Debug {} ...'.format(_to))


    res.insert(0, [num_intersection])
    return res


def main(file_path):
    f = open(file_path, 'r')

    # 첫줄 처리
    line = f.readline()
    D, I, S, V, F = map(int, line.split())

    roadnm_to_path = {}  # 로드 이름 {road : [0, 1]}
    path_to_roadnm = {}  # 경로 이름 {'[0, 2]' : 'road_nm'} 이런식으로 들어감
    # I 개의 인터섹션.
    adj = [[0 for _ in range(I + 1)] for _ in range(I + 1)]  # 그래프

    # intersection 정보들 들어감. (경로정보..)
    for i in range(S):
        line = f.readline()
        start, end, rd_nm, weight = line.split()
        start, end, weight = int(start), int(end), int(weight)
        adj[start][end] = weight
        roadnm_to_path[rd_nm] = [start, end]
        path_to_roadnm['[{}, {}]'.format(start, end)] = rd_nm

    car = []
    # 차 정보 들어감
    for i in range(V):
        line = f.readline()
        line = line.split()
        _, path_nm = line[0], line[1:]
        path = []
        for street in path_nm:
            start, end = roadnm_to_path[street]
            if path:
                path.extend([start, end])
            else:
                path.append(end)
        car.append(path)

    res = solution(D, I, S, V, F, adj, roadnm_to_path, path_to_roadnm, car)

    f = open(file_path[0] + '_submission.txt', 'w')
    for one_res in res:
        try:
            data = ' '.join([str(s) for s in one_res]) + '\n'
        except:
            data = str(one_res) + '\n'
        f.write(data)

    f.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path')
    args = parser.parse_args()

    file_path = args.file_path
    main(file_path)



