from utils import *
import bisect
import sys
import math

class SweepStatusEntry:
    def __init__(self,l):
        # have a line and the point by which it needs to be sorted
        self.l = l

    def __str__(self):
        return "SwapStatusEntry: " + str(self.l)

    # define comparision operations to keep in the sweep status entry
    def __eq__(self,other):
        if (self.l == other.l):
            return True
        return False

    def __ne__(self,other):
        return not self.__eq__(other)

    def __lt__(self,other):
        if check_orientation(other.l.top_point,self.l.top_point,other.l.btm_point) == ANTICLOCKWISE:
            return True
        return False

    def __gt__(self,other):
        if check_orientation(other.l.top_point,self.l.top_point,other.l.btm_point) == CLOCKWISE:
            return True
        return False

class SweepStatus:
    def __init__(self):
        self.lines_list = []
        # all lines as seen by the sweep line

    def find_line(self,l):
        for i in range(len(self.lines_list)):
            if self.lines_list[i].l == l:
                return i

        return None

    def check_intersection(self,l_index,direction):
        res = []
        print("Looking for intersection at index",l_index," direction =",direction)
        cur = l_index #the index of the line which we are checking
        if direction == "left":
            cur = l_index - 1
            while cur >= 0:
                p = intersection_point(self.lines_list[l_index].l,self.lines_list[cur].l)
                if p is not None:
                    res.append(IntersectionPoint(p,self.lines_list[cur].l,self.lines_list[l_index].l))
                else:
                    break
                cur -= 1

        else: # direction is "right"
            cur = l_index + 1
            while cur <= len(self.lines_list)-1:
                p = intersection_point(self.lines_list[l_index].l,self.lines_list[cur].l)
                if p is not None:
                    res.append(IntersectionPoint(p,self.lines_list[l_index].l,self.lines_list[cur].l))
                else:
                    break
                cur += 1
        s = "Found Intersection Point(s): "
        for l in res:
            s += (str(l) + '\n')
        s += "%%%%%%%%%%"
        print(s)
        return res

    def add_line(self,new_l): # return an iterable
        print("Adding line ",new_l)
        res = []

        # insert new one in place
        new_entry = SweepStatusEntry(new_l)

        if len(self.lines_list) == 2:
            print(">> Comparing sweep line stuff <<")

        new_index = bisect.bisect(self.lines_list,new_entry)
        print(new_index)
        self.lines_list = self.lines_list[:new_index] + [new_entry] + self.lines_list[new_index:]
        print("lines list after adding")
        for i in self.lines_list:
            print(i)
            print()

        res.extend(self.check_intersection(new_index,"left"))
        res.extend(self.check_intersection(new_index,"right"))

        return res

    def remove_line(self,l):
        print("Removing line ",l)
        res = []

        l_index = -1
        for i in range(len(self.lines_list)):
            if self.lines_list[i].l == l:
                l_index = i
                break
        if l_index == -1:
            return res

        # remove the line found
        self.lines_list = self.lines_list[:l_index] + self.lines_list[l_index+1:]

        # check for new intersections
        if(len(self.lines_list) != 0):
            res.extend(self.check_intersection(l_index-1,"right"))
            # new l_index is the one that was on the right

        return res

    def intersection_point(self,ipt):
        print("Reached intersection point ",ipt)
        res = []

        l1_index = self.find_line(ipt.l1)
        if (l1_index == None):
            print(self.lines_list[l1_index])
            return res

        l2_index = self.find_line(ipt.l2)
        if (l2_index == None):
            return res

        sw_l1 = SweepStatusEntry(ipt.l1)
        sw_l2 = SweepStatusEntry(ipt.l2)

        print("Swapping indices: ",l1_index,l2_index)

        temp = self.lines_list[l1_index]
        self.lines_list[l1_index] = self.lines_list[l2_index]
        self.lines_list[l2_index] = temp

        print("Lines after swapping: ")
        print(self.lines_list[l1_index])
        print(self.lines_list[l2_index])

        if l1_index > l2_index:
            temp = l1_index
            l1_index = l2_index
            l2_index = temp

        # now l1_index is the lower index

        res.extend(self.check_intersection(l1_index,"left"))
        res.extend(self.check_intersection(l2_index,"right"))

        return res

    def __str__(self):
        s = "--- Sweep Line Status: ---\n"
        for i in self.lines_list:
            s += str(i)
            s += " ;\n"
        s += "-----------------"
        return s

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
            possible_event_points.append((var.ipt,"intersection_point"))
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
                draw_sweep_line(next_point[0].top_point)
            elif next_point[1] == "old_line":
                new_intersections = self.sweep_line_status.remove_line(next_point[0])
                draw_sweep_line(next_point[0].btm_point)
            else:
                new_intersections = self.sweep_line_status.intersection_point(next_point[0])
                draw_sweep_line(next_point[0].ipt)

            self.intersection_points.add(new_intersections)
            self.final_intersection_points.extend([x.ipt for x in new_intersections])

            print(">>>>>>>>> PASS",count,"<<<<<<<<<(start)")
            print(self.line_set)
            print()
            print(self.lines_visited)
            print()
            print(self.intersection_points)
            print()
            print(self.sweep_line_status)
            print(">>>>>>>>> PASS",count,"<<<<<<<<<(end)\n\n")
            count += 1

        print("$$$$$ Final Intersection Points $$$$$")
        for p in self.final_intersection_points:
            print(p)
