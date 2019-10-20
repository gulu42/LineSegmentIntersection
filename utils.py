import math
import sys
from decimal import *
import bisect
import config

COLINEAR = 0
CLOCKWISE = 1
ANTICLOCKWISE = 2

class EmptyCollectionException(BaseException):
    def __init__(self):
        self.args = "Empty Collection"

class SweepCompleteException(BaseException):
    def __init__(self):
        self.args = "Sweep Complete"

# --------------------- sorting functions ---------------------
def key_lines_end_point_y(l):
    return l.btm_point.y

def key_lines_start_point_y(l):
    return l.top_point.y

def key_points_y(p):
    return p.y

# --------------------- other functions ---------------------
def get_round_decimal(x):
    return round(Decimal.from_float(x+0.0),2)

def draw_sweep_line(p):
   config.sweep_y.append(p)

# Derived from the slopes of the lines
def check_orientation(p,q,r):
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)

    if val == 0:
        return COLINEAR
    elif val > 0:
        return CLOCKWISE
    else:
        return ANTICLOCKWISE

def intersection_point(l1,l2):

    print(">>>>>> Entered intersection point calc <<<<<<")

    # Find the orientations of the four points
    o1 = check_orientation(l1.top_point,l1.btm_point,l2.top_point)
    o2 = check_orientation(l1.top_point,l1.btm_point,l2.btm_point)

    o3 = check_orientation(l2.top_point,l2.btm_point,l1.top_point)
    o4 = check_orientation(l2.top_point,l2.btm_point,l1.btm_point)

    print("Orientations: ",o1,o2,o3,o4)

    # general case
    if (o1 != o2) and (o3 != o4):
        print("Lookinf for an intersection point")
        # find intersection point
        m1,c1 = l1.m,l1.c
        m2,c2 = l2.m,l2.c

        if m1 == m2: # parallel lines
            return None

        # Now deal with lines that are parallel to the y-axis
        # Can have only one such line here (l)
        if m1 is None or m2 is None:
            if m1 is None:
                l = l2
                l_perp = l1
            elif m2 is None:
                l = l1
                l_perp = l2
            prop_x = l_perp.top_point.x
            prop_y = (l.m * prop_x) + l.c

        else:
            prop_x = -1 * ((c1 - c2 + 0.0)/(m1 - m2))
            prop_y = (m1 * prop_x) + c1

        return Point(prop_x,prop_y)

    # special case
    if o1 == COLINEAR or o2 == COLINEAR or o3 == COLINEAR or o4 == COLINEAR:
        print("Special case, haven't dealt with it")
        # sys.exit(0)

    return None

def binary_search(l,x):
    i = bisect.bisect_left(l,x)
    if i != len(l) and l[i] == x:
        return i
    return None

# --------------------- Geometric Artifacts ---------------------
class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point(" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self,other):
        x1,y1 = get_round_decimal(self.x),get_round_decimal(self.y)
        x2,y2 = get_round_decimal(other.x),get_round_decimal(other.y)
        if (x1 == x2) and (y1 == y2):
            return True
        return False

    def __ne__(self,other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((get_round_decimal(self.x),get_round_decimal(self.y)))

# not setting the variables externally, once set they are not going to be changed

class Line:
    def __init__(self,p1,p2):
        if p1.x > p2.x:
            p3 = p1
            p1 = p2
            p2 = p3
        # p1 is now the point with the lower x coordinate
        # useful when y-coordinates are equal

        if p1.y >= p2.y:
            self.top_point = p1
            self.btm_point = p2
        else:
            self.top_point = p2
            self.btm_point = p1

        x1,y1 = self.top_point.x,self.top_point.y
        x2,y2 = self.btm_point.x,self.btm_point.y

        if x1 == x2: #line perpendicular to the x axis
            self.m = None
            self.c = None
        else:
            self.m = (y2 - y1 + 0.0)/(x2 - x1)
            self.c = (-1 * x1 * self.m) + y1

    def __str__(self):
        return "Line{ " + str(self.top_point) + " ; " + str(self.btm_point) + " }"

    def __eq__(self,other):
        if (self.top_point == other.top_point) and (self.btm_point == other.btm_point):
            return True
        return False

    def __ne__(self,other):
        return not self.__eq__(other)

# --------------------- Collections ---------------------
# The set of input lines, read out of the file
class LineSet:
    def __init__(self,file_name):
        self.lines = []
        fh = open(file_name,"r")

        s = fh.readline()
        while s != '':
            x1,y1,x2,y2 = map(float,s.split(' '))

            self.lines.append(Line(Point(x1,y1),Point(x2,y2)))

            s = fh.readline()
        self.lines = sorted(self.lines,key = key_lines_start_point_y,reverse = True)
        print("Line set generated. Size = ",len(self.lines))

    def peek(self):
        if len(self.lines) == 0:
            raise EmptyCollectionException
        return self.lines[0]

    def pop(self):
        if len(self.lines) == 0:
            raise EmptyCollectionException
        top_line = self.lines[0]
        self.lines = self.lines[1:]
        return top_line

    def __str__(self):
        s = "--- Line Set: ---\n"
        for i in self.lines:
            s += str(i)
            s += " ;\n"
        s += "-----------------"
        return s

# The collection of lines already visited, so that they can be removed from the sweep line
class SortedCollection:
    def __init__(self):
        self.items = []

    def get_len(self):
        return len(self.items)

    def peek(self):
        if len(self.items) == 0:
            raise EmptyCollectionException
        return self.items[0]

    def pop(self):
        if len(self.items) == 0:
            raise EmptyCollectionException
        top_item = self.items[0]
        self.items = self.items[1:]
        return top_item

    def add(self,l):
        self.items.extend(l)

class VisitedLineSet(SortedCollection):
    def __init__(self):
        super().__init__()

    def add(self,l):
        self.items.extend(l)
        self.items = sorted(self.items,key = key_lines_end_point_y,reverse = True)

    def __str__(self):
        s = "--- Visited Line Set: ---\n"
        for i in self.items:
            s += str(i)
            s += " ;\n"
        s += "-----------------"
        return s

class IntersectionPoint:
    def __init__(self,p,l1,l2):
        self.ipt = p
        self.l1 = l1 # insert l1 as line on the left
        self.l2 = l2 # insert l2 as line on the right

    def key(self):
        return self.ipt.y
        # these points are sorted by y-coordinate

    def __str__(self):
        return ">>Intersection Point<<\n" + str(self.ipt) + "\n" + str(self.l1) + "\n" + str(self.l2)

    def __eq__(self,other):
        # if self.ipt == other.ipt and self.l1 == other.l1 and self.l2 == other.l2:
        if self.ipt == other.ipt:
            return True
        return False

    def __ne__(self,other):
        return not self.__eq__(other)

class IntersectionPointsSet(SortedCollection):
    def __init__(self):
        super().__init__()
        self.all_visited_points = []

    def add(self,l):
        for i in l:
            if i not in self.all_visited_points:
                self.items.append(i)
                self.all_visited_points.append(i)
        self.items = sorted(self.items,key = lambda x: x.key(),reverse = True)

    def __str__(self):
        s = "--- Intersection Points Set: ---\n"
        for i in self.items:
            s += str(i.ipt)
            s += " ;\n"
        s += "-----------------"
        return s
