
# 트리

> Tree : 노드로 이루어진 자료 구조

![img](https://gmlwjd9405.github.io/images/data-structure-tree/tree-terms.png)

- 트리는 하나의 루트 노드를 갖는다.
- 루트 노드는 0개 이상의 자식 노드를 갖는다.
- 비선형 자료구조로 계층적 관계를 표현한다.
- 그래프의 한 종류다. 

```python
# 이진 트리
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
```

## 트리(Tree)와 관련된 용어

- 루트 : 부모노드
- leaf node : 자식이 없는 노드
- 간선(edge) : 노드를 연결하는 선
- 노드의 크기 : 자신을 포함한 모든 자손 노드의 개수
- 노드의 깊이 : 루트 노드에서 어떤 노드에 도달하기 위해 거쳐야 하는 간선의 수
- 노드의 레벨 : 트리의 특정 깊이를 가지는 노드의 집합
- 노드의 차수 : 하위 트리 개수 / 간선수 => 각 노드가 지닌 가지의 수
- 트리의 차수 : 트리의 최대 차수
- 트리의 높이 : 루트 노드에서 가장 깊숙히 있는 노드의 깊이 

## 이진 트리

- 각 노드가 최대 두개 자식을 갖는 트리

### 이진트리의 순회 방법

![img](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbIDSTw%2Fbtq3hnrPpgQ%2FjGpx6PvM60CtpKO23NeI21%2Fimg.png)

1. 전위 순회(preorder)

현재 노드 -> 왼쪽 트리 -> 오른쪽 트리 순서대로 방문하는 방법.

```python
def preorder(root):
    print(root.val)
    preorder(root.left)
    preorfer(root.right)
```

2. 중위 순회 (Inorder)

왼쪽 트리 -> 현재 노드 -> 오른쪽 트리 순서대로 방문하는 방법

```python
def inorder(root):
    inorder(root.left)
    print(root.val)
    inorder(root.right)
```

3. 후위 순회 (Postorder)

왼쪽 트리 -> 오른쪽 트리 -> 현재 노드 순서대로 방문하는 방법

```python
def postorder(root):
    postorder(root.left)
    postorder(root.right)
    print(root.val)
```

4. 레벨 순서 순회 (Level-order)

모든 노드를 낮은 레벨부터 차례대로 순회 = BFS

```python
def level_order(root):
    q = collections.deque([])
    q.append(root)
    while q:
        curr = q.popleft()
        print(curr.val)
        q.append(curr.left)
        q.append(curr.right)
```


## 이진 탐색 트리

> binary search tree

- 모든 노드가 아래와 같은 특정 순서를 따르는 속성이 있는 이진 트리.
- 모든 왼쪽 자식들 <= n < 모든 오른쪽 자식들 


---

> References

- <https://gmlwjd9405.github.io/2018/08/12/data-structure-tree.html>
- <https://butter-shower.tistory.com/223>
