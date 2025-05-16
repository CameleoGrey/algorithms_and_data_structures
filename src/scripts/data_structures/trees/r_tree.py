


"""
An R-Tree is a balanced tree data structure used for spatial indexing, 
similar to a B-tree but designed for multi-dimensional information such as 
rectangles or polygons. It efficiently supports operations like insertion, deletion, and range queries.

This implementation provides a foundational R-Tree suitable for spatial indexing tasks. 
It can be extended with deletion, bulk loading, or more sophisticated splitting strategies for production use.
"""

import random

class Rectangle:
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

    def intersects(self, other):
        return not (self.xmax < other.xmin or self.xmin > other.xmax or
                    self.ymax < other.ymin or self.ymin > other.ymax)

    def contains(self, other):
        return (self.xmin <= other.xmin and self.xmax >= other.xmax and
                self.ymin <= other.ymin and self.ymax >= other.ymax)

    def area(self):
        return (self.xmax - self.xmin) * (self.ymax - self.ymin)

    def expand_to_include(self, other):
        self.xmin = min(self.xmin, other.xmin)
        self.ymin = min(self.ymin, other.ymin)
        self.xmax = max(self.xmax, other.xmax)
        self.ymax = max(self.ymax, other.ymax)

    def __repr__(self):
        return f"Rectangle({self.xmin}, {self.ymin}, {self.xmax}, {self.ymax})"


class Entry:
    def __init__(self, rect, child=None, data=None):
        self.rect = rect
        self.child = child  # For internal nodes
        self.data = data    # For leaf nodes

    def __repr__(self):
        return f"Entry({self.rect}, data={self.data})"

class RTreeNode:
    def __init__(self, max_entries=4, leaf=False):
        self.entries = []
        self.leaf = leaf
        self.max_entries = max_entries
        self.parent = None

    def is_full(self):
        return len(self.entries) >= self.max_entries

    def add_entry(self, entry):
        self.entries.append(entry)
        if self.parent:
            self.parent.update_bounding_rect()

    def get_bounding_rect(self):
        rects = [entry.rect for entry in self.entries]
        if not rects:
            return None
        mbr = Rectangle(rects[0].xmin, rects[0].ymin, rects[0].xmax, rects[0].ymax)
        for rect in rects[1:]:
            mbr.expand_to_include(rect)
        return mbr

    def update_bounding_rect(self):
        # For internal use: update the node's bounding rectangle
        self.bounding_rect = self.get_bounding_rect()

    def __repr__(self):
        return f"RTreeNode(leaf={self.leaf}, entries={self.entries})"

class RTree:
    def __init__(self, max_entries=4):
        self.root = RTreeNode(max_entries=max_entries, leaf=True)
        self.max_entries = max_entries

    def insert(self, rect, data=None):
        leaf = self.choose_leaf(self.root, rect)
        leaf.entries.append(Entry(rect, data=data))
        self.adjust_tree(leaf)

    def choose_leaf(self, node, rect):
        if node.leaf:
            return node
        # Choose the child with the least area enlargement
        best_child = None
        min_enlargement = float('inf')
        for entry in node.entries:
            current_rect = entry.rect
            combined_rect = Rectangle(
                min(current_rect.xmin, rect.xmin),
                min(current_rect.ymin, rect.ymin),
                max(current_rect.xmax, rect.xmax),
                max(current_rect.ymax, rect.ymax)
            )
            enlargement = combined_rect.area() - current_rect.area()
            if enlargement < min_enlargement:
                min_enlargement = enlargement
                best_child = entry.child
        return self.choose_leaf(best_child, rect)

    def adjust_tree(self, node):
        while node:
            if len(node.entries) > node.max_entries:
                node1, node2 = self.split_node(node)
                if node.parent is None:
                    # Create new root
                    new_root = RTreeNode(max_entries=self.max_entries, leaf=False)
                    new_root.entries.append(Entry(node1.get_bounding_rect(), child=node1))
                    new_root.entries.append(Entry(node2.get_bounding_rect(), child=node2))
                    node1.parent = new_root
                    node2.parent = new_root
                    self.root = new_root
                    break
                else:
                    # Add new node to parent
                    parent = node.parent
                    parent.entries.remove(next(e for e in parent.entries if e.child == node))
                    parent.entries.append(Entry(node1.get_bounding_rect(), child=node1))
                    parent.entries.append(Entry(node2.get_bounding_rect(), child=node2))
                    node1.parent = parent
                    node2.parent = parent
                    node = parent
            else:
                node.update_bounding_rect()
                node = node.parent

    def split_node(self, node):
        # Linear split algorithm
        entries = node.entries
        # Pick seeds
        seed1, seed2 = self.pick_seeds(entries)
        node1 = RTreeNode(max_entries=self.max_entries, leaf=node.leaf)
        node2 = RTreeNode(max_entries=self.max_entries, leaf=node.leaf)
        node1.entries.append(seed1)
        node2.entries.append(seed2)
        remaining = [e for e in entries if e != seed1 and e != seed2]

        while remaining:
            if (len(node1.entries) + len(remaining)) == self.max_entries + 1:
                node1.entries.extend(remaining)
                break
            if (len(node2.entries) + len(remaining)) == self.max_entries + 1:
                node2.entries.extend(remaining)
                break
            next_entry = self.pick_next(remaining, node1, node2)
            # Decide where to put the entry
            rect1 = node1.get_bounding_rect()
            rect2 = node2.get_bounding_rect()
            enlargement1 = self.enlargement(rect1, next_entry.rect)
            enlargement2 = self.enlargement(rect2, next_entry.rect)
            if enlargement1 < enlargement2:
                node1.entries.append(next_entry)
            elif enlargement2 < enlargement1:
                node2.entries.append(next_entry)
            else:
                # Tie-breaker: add to the node with smaller area
                if rect1.area() < rect2.area():
                    node1.entries.append(next_entry)
                else:
                    node2.entries.append(next_entry)
            remaining.remove(next_entry)
        return node1, node2

    def pick_seeds(self, entries):
        max_d = -1
        seed1 = seed2 = None
        for i in range(len(entries)):
            for j in range(i + 1, len(entries)):
                rect1 = entries[i].rect
                rect2 = entries[j].rect
                combined = Rectangle(
                    min(rect1.xmin, rect2.xmin),
                    min(rect1.ymin, rect2.ymin),
                    max(rect1.xmax, rect2.xmax),
                    max(rect1.ymax, rect2.ymax)
                )
                d = combined.area() - rect1.area() - rect2.area()
                if d > max_d:
                    max_d = d
                    seed1, seed2 = entries[i], entries[j]
        return seed1, seed2

    def pick_next(self, remaining, node1, node2):
        max_diff = -1
        next_entry = None
        rect1 = node1.get_bounding_rect()
        rect2 = node2.get_bounding_rect()
        for e in remaining:
            d1 = self.enlargement(rect1, e.rect)
            d2 = self.enlargement(rect2, e.rect)
            diff = abs(d1 - d2)
            if diff > max_diff:
                max_diff = diff
                next_entry = e
        return next_entry

    def enlargement(self, rect, new_rect):
        combined = Rectangle(
            min(rect.xmin, new_rect.xmin),
            min(rect.ymin, new_rect.ymin),
            max(rect.xmax, new_rect.xmax),
            max(rect.ymax, new_rect.ymax)
        )
        return combined.area() - rect.area()

    def search(self, search_rect):
        return self._search(self.root, search_rect)

    def _search(self, node, search_rect):
        results = []
        for e in node.entries:
            if e.rect.intersects(search_rect):
                if node.leaf:
                    if search_rect.contains(e.rect):
                        results.append(e.data)
                else:
                    results.extend(self._search(e.child, search_rect))
        return results

# Create an R-Tree
rtree = RTree(max_entries=4)

# Insert some rectangles with associated data
rtree.insert(Rectangle(10, 10, 20, 20), data="Object A")
rtree.insert(Rectangle(15, 15, 25, 25), data="Object B")
rtree.insert(Rectangle(50, 50, 60, 60), data="Object C")
rtree.insert(Rectangle(55, 55, 65, 65), data="Object D")
rtree.insert(Rectangle(70, 70, 80, 80), data="Object E")

# Search within a range
search_area = Rectangle(10, 10, 30, 30)
results = rtree.search(search_area)

print("Objects in search area:", results)
