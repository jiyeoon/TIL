class Solution:
    def findLeaf(self, node):
        res = []
        
        def find_leaf(node):
            nonlocal res
            if not node.left and not node.right:
                res.append(node.val)
                return
            if node.left:
                find_leaf(node.left)
            if node.right:
                find_leaf(node.right)
                
        find_leaf(node)
        return res
        
    def removeLeaf(self, node):
        root = node
        
        def remove_leaf(node):
            if not node.left and not node.right:
                node = None
            else:
                if node.left:
                    node.left = remove_leaf(node.left)
                if node.right:
                    node.right = remove_leaf(node.right)
            return node
        
        remove_leaf(root)
        return root
    
    def findLeaves(self, root: Optional[TreeNode]) -> List[List[int]]:
        res = []
        
        while root:
            res.append(self.findLeaf(root))
            if not root.left and not root.right:
                break
            else:
                root = self.removeLeaf(root)
        
        return res