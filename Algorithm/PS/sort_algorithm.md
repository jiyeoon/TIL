
- [정렬 알고리즘](#정렬-알고리즘)
  - [1. 거품 정렬 (Bubble Sort)](#1-거품-정렬-bubble-sort)
    - [동작 과정](#동작-과정)
    - [예제 코드](#예제-코드)
    - [시간복잡도](#시간복잡도)
  - [2. 선택 정렬 (Selection Sort)](#2-선택-정렬-selection-sort)
    - [동작 과정](#동작-과정-1)
    - [예제 코드](#예제-코드-1)
    - [시간복잡도](#시간복잡도-1)
  - [3. 삽입 정렬 (Insertion Sort)](#3-삽입-정렬-insertion-sort)
    - [동작 과정](#동작-과정-2)
    - [예제 코드](#예제-코드-2)
    - [시간복잡도](#시간복잡도-2)
  - [4. 퀵 정렬 (Quick Sort)](#4-퀵-정렬-quick-sort)
    - [동작 과정](#동작-과정-3)
    - [파이썬 코드](#파이썬-코드)
    - [시간복잡도](#시간복잡도-3)
  - [5. 병합 정렬 (Merge Sort)](#5-병합-정렬-merge-sort)
    - [파이썬 코드로 구현](#파이썬-코드로-구현)
  - [6. 힙정렬 (Heap Sort)](#6-힙정렬-heap-sort)
    - [동작 방식](#동작-방식)
    - [파이썬 코드](#파이썬-코드-1)
    - [시간복잡도](#시간복잡도-4)


# 정렬 알고리즘

## 1. 거품 정렬 (Bubble Sort)

![img](https://github.com/GimunLee/tech-refrigerator/raw/master/Algorithm/resources/bubble-sort-001.gif)

**서로 인접한 두 원소의 대소를 비교하고, 조건에 맞지 않다면 자리를 교환하여 정렬하는 알고리즘**이다.

이름의 유래로는 정렬 과정에서 원소의 이동이 거품이 수면으로 올라오는 듯한 모습을 보이기 때문에 이렇게 지어졌다고 한다.

### 동작 과정

1. 1회전에 첫번째 원소와 두번째 원소를, 두번째 원소와 세번째 원소를, ..... 이런 식으로 마지막-1 번째 원소와 마지막 원소릴 비교하여 조건에 맞지 않는다면 서로 교환한다.
2. 1회전을 수행하고 나면 가장 큰 원소가 맨 뒤로 이동하므로 2회전에서는 맨 끝에 있는 원소는 정렬에서 제외하고, 2회적을 수행하고 나면 끝에서부터 두번째 원소까지는 정렬에서 제외된다. 이렇게 정렬을 1회전 수행할 때 마다 정렬에서 제외되는 데이터가 하나씩 늘어난다.


### 예제 코드

```python
def bubble_sort(arr):
    temp = 0
    for i in range(len(arr)):
        for j in range(len(arr)-i):
            if arr[j-1] > arr[j]:
                # swap하는 부분
                temp = arr[j-1]
                arr[j-1] = arr[j]
                arr[j] = temp
```

### 시간복잡도

$$ O(N^2) $$

시간복잡도를 계산하면 $(n-1) + (n-2) + (n-3) + ... + 2 + 1 = \frac{n(n-1)}{2}$ 이므로 $O(N^2)$가 된다. 또한 Bubbble sort는 정렬 여부에 상관 없이 항상 두개의 원소를 비교하기 때문에 최선, 평균, 최악의 경우 모두 시간복잡도가 동일하다. 


## 2. 선택 정렬 (Selection Sort)

![img](https://github.com/GimunLee/tech-refrigerator/raw/master/Algorithm/resources/selection-sort-001.gif)

Bubble Sort와 유사한 알고리즘으로, **해당 순서에 원소를 넣을 위치는 이미 정해져 있고, 어떤 원소를 넣을지 생각하는 알고리즘**이다.

Selection sort는 배열에서 해당 자리를 선택하고 그 자리에 오는 값을 찾는 것이라고 생각하면 편하다.

### 동작 과정

1. 주어진 배열중에 최솟값을 찾는다.
2. 그 값을 맨 앞에 위치한 값과 교체한다. 
3. 맨 처음 위치를 뺀 나머지 배열을 같은 방법으로 교체한다.


### 예제 코드 


```python
def selection_sort(arr):
    indexmin, temp = 0, 0
    for i in range(len(arr)-1):
        indexmin = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[indexMin]:
                indexmin = j
        # swap
        temp = arr[indexMin]
        arr[indexMin] = arr[i]
        arr[i] = temp
```

### 시간복잡도

$$ O(N^2) $$

데이터의 개수가 n이라고 했을 때 bubble sort와 마찬가지로 $(n-1) + (n-2) + (n-3) + ... + 2 + 1 = \frac{n(n-1)}{2}$ 이므로 $O(N^2)$가 된다. 마찬가지로 최선, 평균, 최악의 경우 모두 시간복잡도는 동일하다.

## 3. 삽입 정렬 (Insertion Sort)

![img](https://github.com/GimunLee/tech-refrigerator/raw/master/Algorithm/resources/insertion-sort-001.gif)

Insertion Sort는 **2번째 원소부터 시작하여 그 앞(왼쪽)의 원소들과 비교하여 삽입할 위치를 지정한 후, 원소를 뒤로 옮기고 지정된 자리에 자료를 삽입**하여 정렬하는 알고리즘이다.

최선의 경우 O(N)이라는 엄청나게 빠른 효율성을 가지고 있어, 다른 정렬 알고리즘의 일부로 사용될 만큼 좋은 정렬 알고리즘이다.

### 동작 과정

1. 정렬은 두번째 위치(index) 값을 temp에 저장한다.
2. temp와 이전에 있는 원소들과 비교하여 삽입해나간다.
3. 1번으로 돌아가 다음 위치(index)의 값을 temp에 저장하고 반복한다.

### 예제 코드

```python
def insertion_sort(arr):
    for index in range(len(arr)):
        temp = arr[index]
        prev = index - 1
        while prev >= 0 and arr[prev] < temp:
            arr[prev+1] = arr[prev]
            prev -= 1
        arr[prev+1] = temp
```

### 시간복잡도

최악의 경우 (역으로 정렬되어있을 경우) $(n-1) + (n-2) + (n-3) + ... + 2 + 1 = \frac{n(n-1)}{2}$ 이므로 $O(N^2)$가 된다. 

하지만 모두 정렬이 되어있는 경우에는 한번씩빢에 비교를 안하므로 $O(N)$의 시간복잡도를 갖는다. 또한, 이미 정렬되어있는 배열에 자료를 하나씩 삽입/제거하는 경우에는 현실적으로 최고의 정렬 알고리즘이 되는데, 탐색을 제외한 오버헤드가 매우 적기 때문이다.


## 4. 퀵 정렬 (Quick Sort)

![img](https://github.com/GimunLee/tech-refrigerator/raw/master/Algorithm/resources/quick-sort-001.gif)

퀵정렬은 **분할 정복(divide and conquer)** 방법을 통해 주어진 배열을 정렬한다.

Quick Sort는 불안정 정렬에 속하며, 다른 원소와의 비교만으로 정렬을 수행하는 비교 정렬에 속한다. 또한 Merge sort와 달리 Quick Sort는 배열을 비균등하게 분할한다.

### 동작 과정

1. 배열 가운데에서 하나의 원소를 고른다. 이렇게 고른 원소를 피벗(pivot)이라고 한다.
2. 피벗 앞에는 피벗보다 값이 작은 모든 원소들이 오고, 피벗 뒤에는 피벗보다 값이 큰 모든 원소들이 오도록 피벗을 기준으로 배열을 둘로 나눈다. 이렇게 배열을 둘로 나누는 것을 **분할(Divide)**라고 한다. 분할을 마친 뒤에 피벗은 더이상 움직이지 않는다.
3. 분할된 두개의 작은 배열에 대해 재귀적으로 이 과정을 반복한다. 


### 파이썬 코드

퀵 정렬은 분할과 정복으로 나누어서 생각할 수 있다.

1. 정복 (Conquer)

부분 배열을 정렬한다. 부분 배열의 크기가 충분히 작지 않으면 순환 호출을 이용하여 다시 분할 정복 방법을 적용한다.

```python
def quickSort(arr, left, right):
    if left >= right:
        return
    
    # 분할
    pivot = partition(arr, left, right)

    # 정복
    quickSort(arr, left, pivot-1)
    quickSort(arr, pivot+1, right)
```

2. 분할 (Divide)

입력 배열을 피벗을 기준으로 비균등하게 2개의 부분 배열로 분할한다.

```python
def partition(arr, left, right):
    pivot = arr[left]
    i, j = left, right

    while i < j:
        while pivot < arr[j]:
            j -= 1
        while i < j and pivot >= arr[i]:
            i += 1
        swap(arr, i, j)
    
    arr[left] = arr[i]
    arr[i] = pivot

    return i
```

더 쉽게..

```python
def quick_sort(arr):
    pivot = arr[len(arr)//2]
    less_arr, equal_arr, greater_arr = [], [], []
    for i in arr:
        if i < pivot:
            less_arr.append(i)
        elif i > pivot:
            greater_arr.append(i)
        else:
            equal_arr.append(i)
    return quick_sort(less_arr) + equal_arr + quick_sort(greater_arr)
```

### 시간복잡도

1. 최선의 경우(Best cases) : T(n) = O(nlog₂n)
   - 비교 횟수 `(log₂n)`
   - 레코드의 개수 n이 2의 거듭제곱이라고 가정(n=2^k) 했을 때, n=2^3의 경우, 2^3 -> 2^2 -> 2^1 -> 2^0 순으로 줄어들어 순환 호출의 깊이가 3임을 알 수 있습니다.
   - 이것을 일반화하면 n=2^k의 경우, **k(k=log₂n)** 임을 알 수 있습니다.
   - 각 순환 호출 단계의 비교 연산 `(n)`
   - 각 순환 호출에서는 전체 리스트의 대부분의 레코드를 비교해야 하므로 **평균 n번** 정도의 비교가 이루어집니다.
   - 따라서, 최선의 시간복잡도는 `순환 호출의 깊이 * 각 순환 호출 단계의 비교 연산 = nlog₂n` 가 됩니다. 이동 횟수는 비교 횟수보다 적으므로 무시할 수 있습니다.

2. 최악의 경우(Worst cases) : T(n) = O(n^2)
   - 최악의 경우는 정렬하고자 하는 배열이 오름차순 정렬되어있거나 내림차순 정렬되어있는 경우입니다. 
   - 비교 횟수 `(n)`
   - 레코드의 개수 n이 2의 거듭제곱이라고 가정(n=2^k)했을 때, 순환 호출의 깊이는 **n** 임을 알 수 있습니다.
   - 각 순환 호출 단계의 비교 연산 `(n)`
   - 각 순환 호출에서는 전체 리스트의 대부분의 레코드를 비교해야 하므로 **평균 n번 ** 정도의 비교가 이루어집니다.
   - 따라서, 최악의 시간복잡도는 `순환 호출의 깊이 * 각 순환 호출 단계의 비교 연산 = n^2` 입니다. 이동 횟수는 비교 횟수보다 적으므로 무시할 수 있습니다.

3. 평균의 경우(Average cases) : T(n) = O(nlog₂n)

## 5. 병합 정렬 (Merge Sort)

![img](https://t1.daumcdn.net/cfile/tistory/9982D83C5C2DDCFE1B)

대표적인 분할정복(Divide and Conquer) 알고리즘.

성능은 퀵정렬보다 전반적으로 뒤떨어지고, 데이터 크기만한 메모리가 더 필요하지만, 최대의 장점은 **데이터의 상태에 별 영향을 받지 않는다**는 점이다. 정렬되어있는 두 배열을 더할 때 이 알고리즘을 사용하면 가장 빠르게 정렬된 상태로 합칠 수 있다.


### 파이썬 코드로 구현

```python
def merge_sort(list):
    if len(list) <= 1:
        return list
    mid = len(list) // 2
    leftList = list[:mid]
    rightList = list[mid:]
    leftList = merge_sort(leftList)
    rightList = merge_sort(rightList)
    return merge(leftList, rightList)
```


## 6. 힙정렬 (Heap Sort)

![img](https://t1.daumcdn.net/cfile/tistory/99F5CD3C5C2DE0F81B)

여기서 힙은 힙트리로, 여러개의 값 들 중 가장 크거나 작은 값을 빠르게 찾기 위해 만든 이진 트리이다. 짧게 힙이라고 부른다.

힙은 항상 완전 이진 트리의 형태를 띈다. 부모의 값은 항상 자식들의 값보다 크거나 (Max Heap) 작아야 (Min Heap) 한다는 규칙이 있다. 따라서 루트(뿌리) 노드에는 항상 데이터들 중 가장 큰 값 혹은 작은 값이 저장되어 있다.


### 동작 방식

힙 정렬의 방법은 아래와 같다.

1. 배열의 원소들을 전부 힙에 삽입
2. 가장 부모노드에 있는 값은 최댓값 혹은 최솟값이므로 루트를 출력하고 힙에서 제거
3. 힙이 빌 때 까지 2의 과정을 반복

힙정렬은 추가적인 메모리를 전혀 필요로하지 않는다는 점과 최악의 경우에도 항상 $O(n \log n)$ 의 성능을 발휘한다는 장점이 있다.

### 파이썬 코드

```python
def heapify(unsorted, index, heap_size):
    largest = index
    left_index = 2 * index + 1
    right_index = 2 * index + 2
    if left_index < heap_size and unsorted[left_index] > unsorted[largest]:
        largest = left_index
    if right_index < heap_size and unsorted[right_index] > unsorted[largest]:
        largest = right_index
    if largest != index:
        unsorted[largest], unsorted[index] = unsorted[index], unsorted[largest]
        heapify(unsorted, largest, heap_size)

def heap_sort(unsorted):
    n = len(unsorted)
    # BUILD-MAX-HEAP (A) : 위의 1단계
    # 인덱스 : (n을 2로 나눈 몫-1)~0
    # 최초 힙 구성시 배열의 중간부터 시작하면 
    # 이진트리 성질에 의해 모든 요소값을 
    # 서로 한번씩 비교할 수 있게 됨 : O(n)
    for i in range(n // 2 - 1, -1, -1):
        heapify(unsorted, i, n)
    # Recurrent (B) : 2~4단계
    # 한번 힙이 구성되면 개별 노드는
    # 최악의 경우에도 트리의 높이(logn)
    # 만큼의 자리 이동을 하게 됨
    # 이런 노드들이 n개 있으므로 : O(nlogn)
    for i in range(n - 1, 0, -1):
        unsorted[0], unsorted[i] = unsorted[i], unsorted[0]
        heapify(unsorted, 0, i)
    return unsorted
```

### 시간복잡도 


$$ O (n \log n) $$