class Solution:
    def isValidBST(self, root: TreeNode) -> bool:
        
        def validate(curr, low=-float('inf'), high=float('inf')):
            if not curr:
                return True

            if curr.val <= low or curr.val >= high:
                return False
            
            return (validate(curr.left, low, curr.val)) and (validate(curr.right, curr.val, high))
        
        return validate(root)
        