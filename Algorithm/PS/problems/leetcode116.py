"""
문제 링크 : https://leetcode.com/problems/populating-next-right-pointers-in-each-node/

# Definition for a Node
class Node:
    def __init__(self, val, left, right, next):
        self.val = val
        self.left = left # Node
        self.right = right
        self.next = next
"""
        
class Solution:
    def connect(self, root):
        if not root or not root.left:
            return root

        root.left.next = root.right
        
        if root.next:
            root.right.next = root.next.left
        
        self.connect(root.left)
        self.connect(root.right)
        
        return root