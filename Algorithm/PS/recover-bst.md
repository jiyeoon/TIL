# 문제 링크 

<https://leetcode.com/problems/recover-binary-search-tree/>

## 문제 코드

```python
import math
class Solution:
    def recoverTree(self, root):
        first, second = None, None
        prev = TreeNode(-math.inf)

        def check(root):
            nonlocal prev, first, second
            if root == None:
                return
            check(root.left)
            if root.val < prev.val:
                if not first:
                    first = prev
                second = root
            prev = root
            check(root.right)
        
        check(root)
        first.val, second.val = second.val, first.val
```