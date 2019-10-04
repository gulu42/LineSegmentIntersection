# sorting functions
def key_lines_end_point_y(l):
    return l.btm_point.y

def key_lines_start_point_y(l):
    return l.top_point.y

def key_points_y(p):
    return p.y

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point: " + str(self.x) + " ; " + str(self.y)

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

        if p1.y <= p2.y:
            self.top_point = p1
            self.btm_point = p2
        else:
            self.top_point = p2
            self.btm_point = p1

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
        self.lines = sorted(self.lines,key = key_lines_start_point_y)

    def get_len(self):
        return len(self.lines) # ideally take care of this in peek, do that later

    def peek(self):
        if len(self.items) == 0:
            raise "EmptyCollectionException"
        return self.lines[0]

    def pop(self):
        if len(self.items) == 0:
            raise "EmptyCollectionException"
        top_line = self.lines[0]
        self.lines = self.lines[1:]
        return top_line

    def __str__(self):
        s = "Line Set: "
        for i in self.lines:
            s += str(i)
            s += " ; "
        return s

# The collection of lines already visited, so that they can be removed from the sweep line
class SortedCollection:
    def __init__(self):
        self.items = []

    def get_len(self):
        return len(self.items)

    def peek(self):
        if len(self.items) == 0:
            raise "EmptyCollectionException"
        return self.items[0]

    def pop(self):
        if len(self.items) == 0:
            raise "EmptyCollectionException"
        top_item = self.items[0]
        self.items = self.items[1:]
        return top_item

    def add_item(self,l):
        self.items.extend(l)

class VisitedLineSet(SortedCollection):
    def __init__(self):
        super(VisitedLineSet,self).__init__()

    def add_item(self,l):
        self.items.extend(l)
        sorted(self.items,key = key_lines_end_point_y)

    def __str__(self):
        s = "Visited Line Set: "
        for i in self.items:
            s += str(i)
            s += " ; "
        return s

class IntersectionPointsSet(SortedCollection):
    def __init__(self):
        super(IntersectionPointsSet,self).__init__()

    def add_item(self,l):
        self.items.extend(l)
        sorted(self.items,key = key_points_y)

    def __str__(self):
        s = "Intersection Points Set: "
        for i in self.items:
            s += str(i)
            s += " ; "
        return s
