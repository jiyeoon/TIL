"""
i번째 블록은 정확히 Li answkfmf vhgkagodi gksek. 
i가 홀수이면 -> 앞 문자보다 더 뒤에 있는 문자로. 
i가 짝수이면 -> 앞 문자보다 더 짧은 그거로. 
"""
"""
def solution(arr):
    res = [0]
    for i, num in enumerate(arr):
        if (i+1) % 2 == 1: # i가 홀수일때 
            for j in range(num-1):
                res.append(res[-1]+1)
            # 마지막에... 뒤에 있는게 있으면...
            if i != len(arr) - 1:
                res.append(max(arr[i+1], res[-1]+1))
            else:
                res.append(res[-1]+1)
        elif (i+1) % 2 == 0:
            if i != len(arr) - 1:
                for j in range(num):
                    res.append(res[-1]-1)
            else:
                for j in range(num):
                    res.append(num-j-1)
    answer = [chr(65+c) for c in res]
    return "".join(answer)

arr = [25, 25, 25]
res = solution(arr)
print(res)

n = int(input())
for i in range(n):
    m = int(input())
    arr = list(map(int, input().split()))
    res = solution(arr)
    print("Case #{}: {}".format(i+1, res))
"""
from collections import deque

def solution(st):
    """
    if st == 'IO' or st == 'OI':
        return 'O', 1
    t = len(st) // 2
    if 'IO' * t + 'I' == st:
        return 'I', 1
    """
    q = deque([])
    q.append([st, 'I'])
    winner = ''
    score = 1
    while q:
        curr, p = q.popleft()
        print(curr, p, len(curr))
        if curr == 'I' and p == 'O':
            winner = 'I'
            score = 2
            break
        if curr == 'O' and p == 'I':
            winner = 'O'
            score = 2
            break
                
        if curr == '':
            if p == 'I':
                winner = 'O'
                score = 1
                break
            else:
                winner = 'I'
                score = 1
                break
        if p == 'I':
            if curr[0] != 'I' and curr[-1] != 'I':
                winner = 'O'
                score += len(curr)
                break
            # leftmost
            if curr[0] == 'I':
                q.append([curr[1:], 'O'])
            # rightmost
            if curr[-1] == 'I':
                q.append([curr[:-1], 'O'])
        elif p == 'O':
            if curr[0] != 'O' and curr[-1] != 'O':
                winner = 'I'
                score += len(curr)
                break
            #leftmost
            if curr[0] == 'O':
                q.append([curr[1:], 'I'])
            #rightmost
            if curr[-1] == 'O':
                q.append([curr[:-1], 'I'])

    return winner, score

w, s = solution('IIIO')
print(w, s)

"""
n = int(input())
for i in range(n):
    st = input()
    winner, score = solution(st)
    print("Case #{}: {} {}".format(i+1, winner, score))
    
"""