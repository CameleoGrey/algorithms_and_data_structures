 
"""
In a Nutshell
A Red-Black Tree is a balanced binary search tree that ensures logarithmic performance for 
key operations by maintaining a specific structure and balancing through rotations and recoloring of nodes.

Overview
A Red-Black Tree is a type of self-balancing binary search tree. It's used to store data in a sorted manner while ensuring 
efficient operations like insertion, deletion, and searching. The "self-balancing" aspect means that the tree automatically 
adjusts its structure to remain balanced, preventing performance degradation to O(n) in the worst-case scenario (which can occur in a regular binary search tree).
Core Principles
A Red-Black Tree adheres to the following properties:

Each node is either red or black.
The root of the tree is always black.
Every leaf (NIL) is black. NIL nodes are special nodes that represent the absence of a node (e.g., when a node doesn't have a left or right child).
If a node is red, then both its children are black. This means that two red nodes cannot be adjacent to each other.
For each node, all paths from that node to any of its descendant NIL nodes contain the same number of black nodes. 
This count is known as the "black-height" of the node.

Why These Properties?
These properties are critical for maintaining the balance of the tree:

Preventing Long Paths: The properties ensure that there is no path from the root to a leaf that is more than twice 
as long as any other path. This is achieved through the red-black coloring and the requirement of an equal number of black nodes on each path.
Limiting Tree Height: The maximum height of a Red-Black Tree with $n$ nodes is $2 \log_2(n+1)$. This ensures that search, 
insertion, and deletion operations are performed in $O(\log n)$ time.

Operations and Balancing
When a node is inserted into or deleted from a Red-Black Tree, the tree's properties might be violated. To restore these properties, 
two primary operations are used:

Rotations:
Left Rotation: Moves a node to the right, promoting its right child to its place.
Right Rotation: Moves a node to the left, promoting its left child to its place.

Recoloring: Changes the color of nodes (from red to black or vice versa) to satisfy the Red-Black Tree properties.

Operation Examples
Insertion
When inserting a new node:
The new node is always added as red.
If the parent of the node is also red, a violation occurs.
In this case, rotations and recoloring are performed to restore the properties.

Deletion
When deleting a node:
If the deleted node was black, the tree's properties might be violated.
In this case, complex rotation and recoloring operations are performed to rebalance the tree.

Advantages of Using Red-Black Trees
Performance: Guaranteed logarithmic time complexity for basic operations.
Efficiency: Well-suited for tasks where insertion, deletion, and search performance are important.
Wide Application: Used in various data structures and algorithms, such as maps and sets in standard libraries of many programming languages.

Explanation
Node Class: Represents each node with data, parent, left, right children, and color.
RedBlackTree Class:
insert(data): Inserts a new node and calls fix_insert to maintain the Red-Black Tree properties.
fix_insert(node): Restructures the tree after insertion by performing rotations and recoloring.
left_rotate(node): Performs a left rotation.
right_rotate(node): Performs a right rotation.
delete_node(data): Deletes a node from the tree.
fix_delete(node): Fixes the tree after deletion to maintain Red-Black Tree properties.
search(data): Searches for a node with the given data.
print_tree(): Prints the tree structure.


Key Concepts
Coloring: Each node is either red or black.
Root Property: The root is always black.
Red Property: If a node is red, then both its children are black.
Black Property: Every path from a given node to any of its descendant NIL nodes contains the same number of black nodes.
This implementation provides a basic Red-Black Tree with insertion, deletion, search, and print functionalities.

"""


class Node:
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.left = None
        self.right = None
        self.color = "red"  # New nodes are always red

class RedBlackTree:
    def __init__(self):
        self.NIL = Node(None)
        self.NIL.color = "black"
        self.root = self.NIL

    def insert(self, data):
        new_node = Node(data)
        new_node.left = self.NIL
        new_node.right = self.NIL

        y = None
        x = self.root

        while x != self.NIL:
            y = x
            if new_node.data < x.data:
                x = x.left
            else:
                x = x.right

        new_node.parent = y

        if y is None:
            self.root = new_node
        elif new_node.data < y.data:
            y.left = new_node
        else:
            y.right = new_node

        if new_node.parent is None:
            new_node.color = "black"
            return

        if new_node.parent.parent is None:
            return

        self.fix_insert(new_node)

    def fix_insert(self, k):
        while k.parent.color == "red":
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left  # uncle
                if u.color == "red":
                    u.color = "black"
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right  # uncle

                if u.color == "red":
                    u.color = "black"
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    self.right_rotate(k.parent.parent)

            if k == self.root:
                break

        self.root.color = "black"

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y

        y.right = x
        x.parent = y

    def delete_node(self, data):
        self.delete_node_helper(self.root, data)

    def delete_node_helper(self, node, key):
        z = self.NIL
        while node != self.NIL:
            if node.data == key:
                z = node

            if node.data <= key:
                node = node.right
            else:
                node = node.left

        if z == self.NIL:
            print("Couldn't find key in the tree")
            return

        y = z
        y_original_color = y.color
        if z.left == self.NIL:
            x = z.right
            self.rb_transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self.rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == "black":
            self.fix_delete(x)

    def fix_delete(self, x):
        while x != self.root and x.color == "black":
            if x == x.parent.left:
                s = x.parent.right
                if s.color == "red":
                    s.color = "black"
                    x.parent.color = "red"
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == "black" and s.right.color == "black":
                    s.color = "red"
                    x = x.parent
                else:
                    if s.right.color == "black":
                        s.left.color = "black"
                        s.color = "red"
                        self.right_rotate(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = "black"
                    s.right.color = "black"
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == "red":
                    s.color = "black"
                    x.parent.color = "red"
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.right.color == "black" and s.left.color == "black":
                    s.color = "red"
                    x = x.parent
                else:
                    if s.left.color == "black":
                        s.right.color = "black"
                        s.color = "red"
                        self.left_rotate(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = "black"
                    s.left.color = "black"
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = "black"

    def rb_transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def minimum(self, node):
        while node.left != self.NIL:
            node = node.left
        return node

    def search(self, data):
        return self.search_helper(self.root, data)

    def search_helper(self, node, data):
        if node == self.NIL or data == node.data:
            return node

        if data < node.data:
            return self.search_helper(node.left, data)
        return self.search_helper(node.right, data)

    def print_tree(self):
        self.print_helper(self.root, "", True)

    def print_helper(self, node, indent, last):
        if node != self.NIL:
            print(indent, end="")
            if last:
                print("R----", end="")
                indent += "     "
            else:
                print("L----", end="")
                indent += "|    "

            s_color = "RED" if node.color == "red" else "BLACK"
            print(str(node.data) + "(" + s_color + ")")
            self.print_helper(node.left, indent, False)
            self.print_helper(node.right, indent, True)


# Test the corrected implementation
tree = RedBlackTree()
values = [10, 18, 7, 15, 16, 30, 25, 40, 60, 2, 1, 70]

for value in values:
    tree.insert(value)

print("Red-Black Tree:")
tree.print_tree()

print("\nSearching for 16:")
if tree.search(16) != tree.NIL:
    print("Found 16")
else:
    print("16 not found")

print("\nDeleting node 10")
tree.delete_node(10)
print("Red-Black Tree after deleting 10:")
tree.print_tree()