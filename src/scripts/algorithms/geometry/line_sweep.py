
"""
The Line Sweep algorithm is a computational geometry technique for solving problems 
involving geometric objects by moving an imaginary line (usually vertical or horizontal) across 
the plane and processing events as the line encounters objects.
"""

import heapq
from collections import namedtuple

import heapq
from collections import namedtuple

# Define data structures
Point = namedtuple('Point', ['x', 'y'])
Event = namedtuple('Event', ['x', 'type', 'segment'])

class LineSweep:
    def __init__(self):
        self.events = []
        self.status = []
        self.intersections = set()

    def add_segment(self, p1, p2):
        """Add a line segment to the sweep."""
        if p1.x > p2.x or (p1.x == p2.x and p1.y > p2.y):
            p1, p2 = p2, p1
        segment = (p1, p2)
        
        # Add segment endpoints as events
        heapq.heappush(self.events, Event(p1.x, 'left', segment))
        heapq.heappush(self.events, Event(p2.x, 'right', segment))

    def find_intersections(self):
        """Find all intersections between segments."""
        while self.events:
            event = heapq.heappop(self.events)
            
            if event.type == 'left':
                self._handle_left_event(event)
            elif event.type == 'right':
                self._handle_right_event(event)
            else:  # intersection event
                self._handle_intersection_event(event)
        
        return self.intersections

    def _handle_left_event(self, event):
        """Process a left endpoint event."""
        segment = event.segment
        # Insert into status maintaining order
        self._insert_into_status(segment)
        
        # Get neighbors and check for intersections
        index = self.status.index(segment)
        if index > 0:
            self._check_intersection(segment, self.status[index-1])
        if index < len(self.status) - 1:
            self._check_intersection(segment, self.status[index+1])

    def _handle_right_event(self, event):
        """Process a right endpoint event."""
        segment = event.segment
        index = self.status.index(segment)
        
        # Check for intersection between new neighbors
        if index > 0 and index < len(self.status) - 1:
            self._check_intersection(self.status[index-1], self.status[index+1])
        
        # Remove segment from status
        self.status.remove(segment)

    def _handle_intersection_event(self, event):
        """Process an intersection event."""
        seg1, seg2 = event.segment
        if seg1 not in self.status or seg2 not in self.status:
            return
            
        # Add the intersection point
        intersect = self._compute_intersection(seg1, seg2)
        if intersect:
            self.intersections.add(intersect)
            
        # Swap the segments in the status
        index1 = self.status.index(seg1)
        index2 = self.status.index(seg2)
        if abs(index1 - index2) != 1:
            return  # segments not adjacent
            
        self.status[index1], self.status[index2] = self.status[index2], self.status[index1]
        
        # Check new neighbors for intersections
        if index1 < index2:
            if index1 > 0:
                self._check_intersection(self.status[index1], self.status[index1-1])
            if index2 < len(self.status) - 1:
                self._check_intersection(self.status[index2], self.status[index2+1])
        else:
            if index2 > 0:
                self._check_intersection(self.status[index2], self.status[index2-1])
            if index1 < len(self.status) - 1:
                self._check_intersection(self.status[index1], self.status[index1+1])

    def _insert_into_status(self, segment):
        """Insert a segment into the status maintaining proper order."""
        # Binary search to find insertion point
        low, high = 0, len(self.status)
        while low < high:
            mid = (low + high) // 2
            if self._above(segment, self.status[mid]):
                low = mid + 1
            else:
                high = mid
        self.status.insert(low, segment)

    def _above(self, seg1, seg2):
        """Check if seg1 is above seg2 at current x position."""
        x = max(seg1[0].x, seg2[0].x)
        y1 = self._get_y_at_x(seg1, x)
        y2 = self._get_y_at_x(seg2, x)
        return y1 > y2 if y1 != y2 else seg1[0].y > seg2[0].y

    def _get_y_at_x(self, segment, x):
        """Get y-coordinate of segment at given x."""
        p1, p2 = segment
        if p1.x == p2.x:  # Vertical line
            return float('inf') if p1.y < p2.y else float('-inf')
        
        # Linear interpolation
        return p1.y + (p2.y - p1.y) * (x - p1.x) / (p2.x - p1.x)

    def _check_intersection(self, seg1, seg2):
        """Check if two segments intersect and add to results if they do."""
        intersect = self._compute_intersection(seg1, seg2)
        if intersect and intersect.x > heapq.nsmallest(1, self.events)[0].x if self.events else float('-inf'):
            heapq.heappush(self.events, Event(intersect.x, 'intersection', (seg1, seg2)))

    def _compute_intersection(self, seg1, seg2):
        """Compute intersection point of two segments if it exists."""
        p1, p2 = seg1
        p3, p4 = seg2
        
        # Line segments as parametric equations
        denom = (p4.y - p3.y) * (p2.x - p1.x) - (p4.x - p3.x) * (p2.y - p1.y)
        if denom == 0:  # Parallel lines
            return None
            
        ua = ((p4.x - p3.x) * (p1.y - p3.y) - (p4.y - p3.y) * (p1.x - p3.x)) / denom
        ub = ((p2.x - p1.x) * (p1.y - p3.y) - (p2.y - p1.y) * (p1.x - p3.x)) / denom
        
        if 0 <= ua <= 1 and 0 <= ub <= 1:
            x = p1.x + ua * (p2.x - p1.x)
            y = p1.y + ua * (p2.y - p1.y)
            return Point(x, y)
        return None

# Create line segments
segments = [
    (Point(1, 1), Point(5, 5)),
    (Point(1, 5), Point(5, 1)),
    (Point(2, 0), Point(2, 6)),
    (Point(0, 3), Point(6, 3))
]

##################################################################################
# Find all intersections
sweep = LineSweep()
for seg in segments:
    sweep.add_segment(*seg)

intersections = sweep.find_intersections()
print("Intersections found:")
for p in intersections:
    print(f"({p.x:.2f}, {p.y:.2f})")


##################################################################################
Rectangle = namedtuple('Rectangle', ['x1', 'y1', 'x2', 'y2'])

def find_rectangle_overlaps(rectangles):
    """Find all overlapping regions between rectangles using line sweep."""
    events = []
    
    # Create vertical edges as events
    for rect in rectangles:
        events.append((rect.x1, 'start', rect))
        events.append((rect.x2, 'end', rect))
    
    # Sort events by x-coordinate
    events.sort()
    
    active = []
    overlaps = []
    
    for event in events:
        x, typ, rect = event
        
        if typ == 'start':
            # Check for intersections with active rectangles
            for active_rect in active:
                overlap = _rectangles_overlap(rect, active_rect)
                if overlap:
                    overlaps.append(overlap)
            active.append(rect)
        else:
            active.remove(rect)
    
    return overlaps

def _rectangles_overlap(r1, r2):
    """Check if two rectangles overlap and return overlap region."""
    x_overlap = max(0, min(r1.x2, r2.x2) - max(r1.x1, r2.x1))
    y_overlap = max(0, min(r1.y2, r2.y2) - max(r1.y1, r2.y1))
    
    if x_overlap > 0 and y_overlap > 0:
        return Rectangle(
            max(r1.x1, r2.x1),
            max(r1.y1, r2.y1),
            min(r1.x2, r2.x2),
            min(r1.y2, r2.y2)
        )
    return None

# Usage
rectangles = [
    Rectangle(1, 1, 4, 4),
    Rectangle(3, 3, 6, 6),
    Rectangle(2, 2, 5, 5)
]

overlaps = find_rectangle_overlaps(rectangles)
print("\nRectangle overlaps:")
for overlap in overlaps:
    print(f"({overlap.x1}, {overlap.y1}) to ({overlap.x2}, {overlap.y2})")

##################################################################################
import math

def closest_pair(points):
    """Find the closest pair of points using line sweep."""
    points.sort()  # Sort by x-coordinate
    min_dist = float('inf')
    closest = None
    active = []
    
    for point in points:
        # Remove points too far away
        while active and (point.x - active[0].x) > min_dist:
            active.pop(0)
        
        # Check against points in active set (sorted by y-coordinate)
        for other in active:
            dist = math.sqrt((point.x - other.x)**2 + (point.y - other.y)**2)
            if dist < min_dist:
                min_dist = dist
                closest = (point, other)
        
        # Insert point maintaining y-order
        i = 0
        while i < len(active) and active[i].y < point.y:
            i += 1
        active.insert(i, point)
    
    return closest, min_dist

# Usage
points = [
    Point(1, 2),
    Point(3, 4),
    Point(5, 1),
    Point(6, 3),
    Point(8, 2),
    Point(9, 5)
]

pair, distance = closest_pair(points)
print(f"\nClosest pair: ({pair[0].x}, {pair[0].y}) and ({pair[1].x}, {pair[1].y})")
print(f"Distance: {distance:.2f}")