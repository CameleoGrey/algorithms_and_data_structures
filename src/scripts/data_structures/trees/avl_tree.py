
"""
AVL (Adelson-Velsky and Landis) Trees are self-balancing binary search trees that maintain a 
height balance property (the heights of the left and right subtrees of any node differ by at most 1). 
This ensures O(log n) time complexity for insertion, deletion, and search operations.

Key Takeaways
Balancing Mechanism:
AVL trees rotate (left/right) when the balance factor (left height - right height) is > 1 or < -1.
Ensures O(log n) time for all operations.
Insertion & Deletion:
Follows BST rules first.
After insertion/deletion, rebalance if needed.

Use Cases:
When frequent searches are needed (better than Red-Black Trees for lookup-heavy tasks).
Used in databases, filesystems, and memory allocation.

Comparison with Red-Black Trees:
AVL Trees are more strictly balanced → faster lookups.
Red-Black Trees have fewer rotations → better for frequent insertions/deletions.
"""


class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1  # Height of the node (leaf nodes have height 1)

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        """Public method to insert a key into the AVL Tree."""
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        """Recursively insert a key and balance the tree."""
        # Step 1: Perform standard BST insertion
        if not node:
            return AVLNode(key)
        elif key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        # Step 2: Update height of the current node
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # Step 3: Get the balance factor
        balance = self._get_balance(node)

        # Step 4: Rebalance if needed (4 cases)
        # Left Left Case (Right Rotation)
        if balance > 1 and key < node.left.key:
            return self._right_rotate(node)

        # Right Right Case (Left Rotation)
        if balance < -1 and key > node.right.key:
            return self._left_rotate(node)

        # Left Right Case (Left-Right Rotation)
        if balance > 1 and key > node.left.key:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # Right Left Case (Right-Left Rotation)
        if balance < -1 and key < node.right.key:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def delete(self, key):
        """Public method to delete a key from the AVL Tree."""
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        """Recursively delete a key and balance the tree."""
        # Step 1: Perform standard BST delete
        if not node:
            return node

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Node with only one child or no child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Node with two children: Get inorder successor (smallest in right subtree)
            temp = self._get_min_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)

        # If the tree had only one node, return
        if node is None:
            return node

        # Step 2: Update height
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # Step 3: Get balance factor
        balance = self._get_balance(node)

        # Step 4: Rebalance if needed
        # Left Left Case
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._right_rotate(node)

        # Right Right Case
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._left_rotate(node)

        # Left Right Case
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # Right Left Case
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def search(self, key):
        """Search for a key in the AVL Tree."""
        return self._search(self.root, key)

    def _search(self, node, key):
        """Recursively search for a key."""
        if not node:
            return False
        if key == node.key:
            return True
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def _get_height(self, node):
        """Get the height of a node (handles None case)."""
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        """Get the balance factor of a node (left height - right height)."""
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _left_rotate(self, z):
        """Left rotation around node z."""
        y = z.right
        T2 = y.left

        # Perform rotation
        y.left = z
        z.right = T2

        # Update heights
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _right_rotate(self, z):
        """Right rotation around node z."""
        y = z.left
        T3 = y.right

        # Perform rotation
        y.right = z
        z.left = T3

        # Update heights
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def _get_min_node(self, node):
        """Get the node with the smallest key in the subtree."""
        current = node
        while current.left:
            current = current.left
        return current

    def inorder_traversal(self):
        """Print the tree in inorder (sorted order)."""
        self._inorder(self.root)
        print()

    def _inorder(self, node):
        """Recursively traverse in inorder."""
        if node:
            self._inorder(node.left)
            print(node.key, end=" ")
            self._inorder(node.right)

    def print_tree(self):
        """Print the tree structure (for visualization)."""
        self._print_tree(self.root, "", True)

    def _print_tree(self, node, indent, last):
        """Recursively print the tree structure."""
        if node:
            print(indent, end="")
            if last:
                print("R----", end="")
                indent += "     "
            else:
                print("L----", end="")
                indent += "|    "
            print(node.key)
            self._print_tree(node.left, indent, False)
            self._print_tree(node.right, indent, True)

if __name__ == "__main__":
    avl = AVLTree()

    # Insert keys
    keys = [10, 20, 30, 40, 50, 25]
    for key in keys:
        avl.insert(key)

    # Print the tree structure
    print("AVL Tree Structure:")
    avl.print_tree()

    # Inorder traversal (sorted order)
    print("\nInorder Traversal (Sorted Order):")
    avl.inorder_traversal()

    # Search for a key
    search_key = 30
    print(f"\nSearch for {search_key}: {'Found' if avl.search(search_key) else 'Not Found'}")

    # Delete a key
    delete_key = 20
    avl.delete(delete_key)
    print(f"\nAfter Deleting {delete_key}:")
    avl.print_tree()