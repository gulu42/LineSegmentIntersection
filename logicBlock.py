from utils import *
# not a very good practice but its okay for now

class SweepStatus:
    def __init__(self):
        self.temp_point = Point(1,2)
        self.lines_list = []

    def add_line(self,new_l): # return an iterable
        print("Adding line ",new_l)
        # found_greater = False
        # i = 0
        # for i in range(len(self.lines_list)):
        #     l = self.lines_list[i]
        #     if
        #
        # self.lst.append(l)
        # if len(self.lst) == 2:
        #     print("><><><><><><><>< Intersection Point: ", self.lst[0].intersection(l))
        return [self.temp_point]

    def remove_line(self,l):
        print("Removing line ",l)
        self
        return [self.temp_point]

    def intersection_point(self,p):
        print("Reached intersection point ",p)
        return [self.temp_point]

class Sweeper:
    def __init__(self, file_name = "data_1.txt"):
        self.line_set = LineSet(file_name)
        self.lines_visited = VisitedLineSet()
        self.intersection_points = IntersectionPointsSet()
        self.final_intersection_points = []
        self.sweep_line_status = SweepStatus()
        print(">>>>>>> ",self.line_set)
        print("Initialized sweeper")

    def get_next_event_point(self):
        possible_event_points = []
        try:
            var = self.line_set.peek() # newest element sorted by top point
            possible_event_points.append((var.top_point,"new_line"))
        except EmptyCollectionException:
            pass

        try:
            var = self.lines_visited.peek()
            possible_event_points.append((var.btm_point,"old_line"))
        except EmptyCollectionException:
            pass

        try:
            var = self.intersection_points.peek()
            possible_event_points.append((var,"intersection_point"))
        except EmptyCollectionException:
            pass

        possible_event_points = sorted(possible_event_points,key = lambda x: x[0].y,reverse = True) # get earliest point going by y coordinate (highest y)

        if len(possible_event_points) == 0:
            raise SweepCompleteException

        next_point = possible_event_points[0]
        if next_point[1] == "new_line":
            return (self.line_set.pop(),"new_line")
        elif next_point[1] == "old_line":
            return (self.lines_visited.pop(),"old_line")
        else:
            return (self.intersection_points.pop(),"intersection_point")


    def run(self):
        count = 1
        while 1:
            try:
                next_point = self.get_next_event_point()
            except SweepCompleteException:
                print("Sweeping complete")
                return self.final_intersection_points

            if next_point[1] == "new_line":
                new_intersections = self.sweep_line_status.add_line(next_point[0])
                self.lines_visited.add([next_point[0]])
            elif next_point[1] == "old_line":
                new_intersections = self.sweep_line_status.remove_line(next_point[0])
            else:
                new_intersections = self.sweep_line_status.intersection_point(next_point[0])

            print(">>>>>>>>> PASS",count,"<<<<<<<<<(start)")
            print(self.line_set)
            print()
            print(self.lines_visited)
            print()
            print(self.intersection_points)
            print(">>>>>>>>> PASS",count,"<<<<<<<<<(end)\n\n")
            count += 1
            # self.intersection_points.add(new_intersections)
            # self.final_intersection_points.extend(new_intersections)
