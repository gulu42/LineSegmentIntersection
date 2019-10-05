# sorting functions
def key_lines_end_point_y(l):
    return l.btm_point.y

def key_lines_start_point_y(l):
    return l.top_point.y

def key_points_y(p):
    return p.y

class EmptyCollectionException(BaseException):
    def __init__(self):
        self.args = "Empty Collection"

class SweepCompleteException(BaseException):
    def __init__(self):
        self.args = "Sweep Complete"

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point: (" + str(self.x) + ", " + str(self.y) + ")"

    def __eq__(self,other):
        if (self.x == other.x) and (self.y == other.y):
            return True
        return False

    def __ne__(self,other):
        return not self.__eq__(other)

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

        if x1 == x2: #points perpendicular to the x axis
            self.m = None
            self.c = None
        else:
            self.m = (y2 - y1 + 0.0)/(x2 - x1)
            self.c = (-1 * x1 * self.m) + y1

    # use within the class, to check if a point on the line lies within the segment given it lies on the line
    def point_on_segment(self,p):
        if self.top_point.x == self.btm_point.x: # a verticle line
            if (self.top_point.y > p.y) and (self.btm_point.y < p.y):
                return True
        elif self.top_point.x < self.btm_point.x: #downwards, not using slope since that might be null
            if (p.x >= self.top_point.x) and (p.x <= self.btm_point.x):
                return True
        else:
            if (p.x <= self.top_point.x) and (p.x >= self.btm_point.y):
                return True
        return False

    def intersection(self,l2):
        m1,c1 = self.m,self.c
        m2,c2 = l2.m,l2.c

        if m1 == m2: # parallel lines
            return None

        # Now deal with lines that are parallel to the y-axis
        # Can have only one such line here (l)
        if m1 is None or m2 is None:
            if m1 is None:
                l = l2
                l_perp = self
            elif m2 is None:
                l = self
                l_perp = l2
            prop_x = l_perp.top_point.x
            prop_y = (l.m * prop_x) + l.c

        else:
            prop_x = -1 * ((c1 - c2 + 0.0)/(m1 - m2))
            prop_y = (m1 * prop_x) + c1

        prop_point = Point(prop_x,prop_y)
        if self.point_on_segment(prop_point) and l2.point_on_segment(prop_point):
            return prop_point
        else:
            return None

    def __str__(self):
        return "Line: " + str(self.top_point) + " ; " + str(self.btm_point)

    def __eq__(self,other):
        if (self.top_point == other.top_point) and (self.btm_point == other.btm_point):
            return True
        return False

    def __ne__(self,other):
        return not self.__eq__(other)

# The set of input lines, read out of the file
class LineSet:
    def __init__(self,file_name):
        self.lines = []
        fh = open("data_files/" + file_name,"r")

        s = fh.readline()
        while s != '':
            x1,y1,x2,y2 = map(float,s.split(' '))

            self.lines.append(Line(Point(x1,y1),Point(x2,y2)))

            s = fh.readline()
        self.lines = sorted(self.lines,key = key_lines_start_point_y,reverse = True)
        print("Line set generated. Size = ",len(self.lines))

    def get_len(self):
        return len(self.lines) # ideally take care of this in peek, do that later

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

class IntersectionPointsSet(SortedCollection):
    def __init__(self):
        super().__init__()

    def add(self,l):
        self.items.extend(l)
        self.items = sorted(self.items,key = key_points_y,reverse = True)

    def __str__(self):
        s = "--- Intersection Points Set: ---\n"
        for i in self.items:
            s += str(i)
            s += " ;\n"
        s += "-----------------"
        return s
