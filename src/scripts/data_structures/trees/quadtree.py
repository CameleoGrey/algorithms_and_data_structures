class Point:
    def __init__(self, x, y, data=None):
        self.x = x
        self.y = y
        self.data = data

    def __repr__(self):
        return f"Point({self.x}, {self.y}, {self.data})"


class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x  # Center x
        self.y = y  # Center y
        self.width = width
        self.height = height

    def contains(self, point):
        return (self.x - self.width / 2 <= point.x <= self.x + self.width / 2 and
                self.y - self.height / 2 <= point.y <= self.y + self.height / 2)

    def intersects(self, range):
        return not (range.x - range.width / 2 > self.x + self.width / 2 or
                    range.x + range.width / 2 < self.x - self.width / 2 or
                    range.y - range.height / 2 > self.y + self.height / 2 or
                    range.y + range.height / 2 < self.y - self.height / 2)

"""
A Quadtree is a tree data structure used to partition a two-dimensional space by 
recursively subdividing it into four quadrants or regions. It is especially useful 
for spatial indexing, collision detection, and image processing.

This implementation can be extended for more complex spatial operations or 
optimized for performance depending on your specific needs.
"""

class Quadtree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary  # Rectangle
        self.capacity = capacity  # Max points before subdivision
        self.points = []
        self.divided = False

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.width / 2
        h = self.boundary.height / 2

        ne = Rectangle(x + w / 2, y - h / 2, w, h)
        nw = Rectangle(x - w / 2, y - h / 2, w, h)
        se = Rectangle(x + w / 2, y + h / 2, w, h)
        sw = Rectangle(x - w / 2, y + h / 2, w, h)

        self.northeast = Quadtree(ne, self.capacity)
        self.northwest = Quadtree(nw, self.capacity)
        self.southeast = Quadtree(se, self.capacity)
        self.southwest = Quadtree(sw, self.capacity)

        self.divided = True

    def insert(self, point):
        if not self.boundary.contains(point):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()

            if self.northeast.insert(point):
                return True
            elif self.northwest.insert(point):
                return True
            elif self.southeast.insert(point):
                return True
            elif self.southwest.insert(point):
                return True

        return False

    def query(self, range, found=None):
        if found is None:
            found = []

        if not self.boundary.intersects(range):
            return found
        else:
            for p in self.points:
                if range.contains(p):
                    found.append(p)
            if self.divided:
                self.northwest.query(range, found)
                self.northeast.query(range, found)
                self.southwest.query(range, found)
                self.southeast.query(range, found)
        return found

# Define boundary of the quadtree
boundary = Rectangle(0, 0, 200, 200)
qt = Quadtree(boundary, capacity=4)

# Insert some points
points = [Point(10, 10), Point(-20, -20), Point(50, 50), Point(-60, 80), Point(70, -70)]
for p in points:
    qt.insert(p)

# Query points within a range
search_area = Rectangle(0, 0, 100, 100)
found_points = qt.query(search_area)

print("Points found in range:", found_points)
