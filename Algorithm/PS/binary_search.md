
# Binary Search

> 이진탐색이란? 

**데이터가 정렬되어 있는 배열**에서 특정한 값을 찾아내는 알고리즘. 배열의 중간에 있는 임의의 값을 선택하여 찾고자 하는 값 x와 비교한다. x가 중간값보다 작으면 중간 값을 기준으로 좌측의 데이터들을, x가 중간값보다 크면 배열의 우측을 대상으로 다시 탐색한다. 

- 순차 탐색 : 리스트 안에 있는 특정한 데이터를 찾기 위해 앞에서부터 하나씩 확인
- 이진 탐색 : 정렬되어있는 리스트에서 탐색 범위를 절반씩 좁혀가며 데이터를 탐색

## 예시

이미 정렬되어있는 10개의 데이터 중에서 4인 원소를 찾는다고 해보자.

![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FeBUyIW%2FbtqSmBuZfNc%2F728Fa21EhKHBxb8eyoOSK1%2Fimg.png)

![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcH0ww3%2FbtqSmAbNllJ%2FXKxSkfYVpEw0Ex0bTOEUU1%2Fimg.png)

![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FPrlOJ%2FbtqSxBOrddX%2FFRzRKyNz4xk5cP4vKgrL9K%2Fimg.png)

![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FlaClf%2FbtqSmAQmJCt%2FjMnfB4oOuSTFCeSz9TTkkK%2Fimg.png)


## 이진 탐색의 시간 복잡도

- 단계마다 탐색 범위를 2로 나누는 것과 동일하므로 연산 횟수는 $ O(\log_{2} N)$ 
- 탐색 범위를 절반씩 줄여나가므로 시간 복잡도는 $ O(\logN) $을 보장한다.


## 코드 구현

### 1. 재귀로 구현

```python
def binary_search(array, target, start, end):
    if start > end:
        return None
    mid = (start + end) // 2
    if array[mid] == target:
        return mid
    elif array[mid] > target:
        return binary_search(array, target, start, mid-1)
    elif array[mid] < target:
        return binary_search(array, target, mid+1, end)
```

### 2. 반복문으로 구현

```python
def binary_search(array, target, start, end):
    while start <= end:
        mid = (start + end) //2
        if array[mid] == target:
            return mid
        elif array[mid] > target:
            end = mid - 1
        elif array[mid] < target:
            start = mid + 1
    return None
```

