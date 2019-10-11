# just stuff im too scared to delete but i want to get rif of the mess

def is_clockwise(p1,p2,p3):
    try:
        sigma = (p2.y - p1.y + 0.0)/(p2.x - p1.x)
    except ZeroDivisionError:
        sigma = math.inf

    try:
        tau = (p3.y - p2.y + 0.0)/(p3.x - p2.x)
    except ZeroDivisionError:
        tau = math.inf

    if sigma > tau:
        return True
    return False

def is_anticlockwise(p1,p2,p3):
    try:
        sigma = (p2.y - p1.y + 0.0)/(p2.x - p1.x)
    except ZeroDivisionError:
        sigma = math.inf

    try:
        tau = (p3.y - p2.y + 0.0)/(p3.x - p2.x)
    except ZeroDivisionError:
        tau = math.inf

    if sigma < tau:
        return True
    return False

# sweep status entry
# def __le__(self,other):
#     if self.key_point.x <= other.key_point.x:
#         return True
#     return False

# def __ge__(self,other):
#     if self.key_point.x >= other.key_point.x:
#         return True
#     return False

def __lt__(self,other):
    if check_orientation(other.l.top_point,self.l.top_point,other.l.btm_point) == ANTICLOCKWISE:
        return True
    return False
    # return SweepStatusEntry.is_anticlockwise(other.l.top_point,self.l.top_point,other.l.btm_point)

def __gt__(self,other):
    if check_orientation(other.l.top_point,self.l.top_point,other.l.btm_point) == CLOCKWISE:
        return True
    return False
    # return SweepStatusEntry.is_clockwise(other.l.top_point,self.l.top_point,other.l.btm_point)

# class line
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
        print(">> POINT PROPOSAL:",prop_point)
        print(self.point_on_segment(prop_point))
        print(l2.point_on_segment(prop_point))
        if self.point_on_segment(prop_point) and l2.point_on_segment(prop_point):
            return prop_point
        else:
            return None

# line set
    def get_len(self):
        return len(self.lines) # ideally take care of this in peek, do that later
