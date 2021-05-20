class Solution:
    def pathSum(self, root: TreeNode, targetSum: int) -> List[List[int]]:
        if not root:
            return []
        
        res = []
        
        def dfs(curr, val, path):
            nonlocal res
            
            if (not curr.left) and (not curr.right):
                tmp = val + curr.val
                pth = path + [curr.val]
                if tmp == targetSum:
                    res.append(pth)
                return
            
            if curr.left:
                dfs(curr.left, val + curr.val, path + [curr.val])
            if curr.right:
                dfs(curr.right, val + curr.val, path + [curr.val])
        
        dfs(root, 0, [])
        #print(res)
        return res