def solution(arr):
    res = [0]
    for i, num in enumerate(arr):
        if (i+1) % 2 == 1: # i가 홀수일때 
            for j in range(num-1):
                res.append(res[-1]+1)
            if i != len(arr) - 1:
                res.append(max(arr[i+1], res[-1]+1))
            else:
                res.append(res[-1]+1)
        elif (i+1) % 2 == 0:
            for j in range(num):
                res.append(num-j-1)
            """
            if i != len(arr) - 1: # 마지막이 아니면.. 
                for j in range(num):
                    res.append(res[-1]-1)
            else: # 마지막이면.. 
                for j in range(num):
                    res.append(num-j-1)
            """
    answer = [chr(65+c) for c in res]
    return "".join(answer)

res = solution([2])
print(res)
print(len(res), 1+sum([2, 4, 5, 5]))