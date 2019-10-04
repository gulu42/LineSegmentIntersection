from utils import *
# not a very good practice but its okay for now

class SweepStatus:
    def __init__(self):
        pass

    def add_line(self,l): # return an iterable
        pass

    def remove_line(self,l):
        pass

    def intersection_point(self,p):
        pass

class Sweeper:
    def __init__(self, file_name = "data_1.txt"):
        self.line_set = LineSet(file_name)
        self.lines_visited = VisitedLineSet()
        self.intersection_points = IntersectionPointsSet()
        self.final_intersection_points = []
        self.sweep_line_status = SweepStatus()

    def get_next_event_point():
        possible_event_points = []
        try:
            var = line_set.peek() # newest element sorted by top point
            possible_event_points.append((var.top_point,"new_line"))
        except "EmptyCollectionException":
            pass

        try:
            var = lines_visited.peek()
            possible_event_points.append((var.btm_point,"old_line"))
        except "EmptyCollectionException":
            pass

        try:
            var = intersection_points.peek()
            possible_event_points.append((var,"intersection_point"))
        except "EmptyCollectionException":
            pass

        possible_event_points = sorted(possible_event_points,key = lambda x: x[0].y) # get earliest point going by y coordinate

        if len(possible_event_points) == 0:
            raise "SweepComplete"

        next_point = possible_event_points[0]
        if next_point[1] == "new_line":
            return (line_set.pop(),"new_line")
        elif next_point[1] == "old_line":
            return (lines_visited.pop(),"old_line")
        else:
            return (intersection_points.pop(),"intersection_point")


    def run():
        try:
            next_point = get_next_event_point()
        except "SweepComplete":
            print "Sweeping complete"
            return self.final_intersection_points

        if next_point[1] == "new_line":
            new_intersections = sweep_line_status.add_line(next_point[0])
        elif next_point[1] == "old_line":
            new_intersections = sweep_line_status.remove_line(next_point[0])
        else:
            new_intersections = sweep_line_status.intersection_point(next_point[0])

# update sweepline properly and i need the seperate class to calculate the intersection points for me

# add self everywhere
