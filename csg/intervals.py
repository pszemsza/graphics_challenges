import math

# Possible relations between 2 intervals.
# Describes position of the second interval in relation to the first.
_NON_OVERLAPPING_LEFT = 1
_NON_OVERLAPPING_RIGHT = 2
_OVERLAPPING_LEFT = 3
_OVERLAPPING_RIGHT = 4
_CONTAINED_WITHIN = 5
_CONTAINS = 6
_EQUALS = 7


class Interval:
    def __init__(self, a=0, b=0, ia=None, ib=None, is_empty=False):
        self.a = a
        self.b = b
        self.ia = ia
        self.ib = ia if ib is None else ib
        self.is_empty = is_empty

    def __str__(self):
        return "({0}, {1}; ind: {2}, {3})".format(self.a, self.b, self.ia, self.ib)

    def copy(self):
        return Interval(self.a, self.b)
    
    def equals(self, interval):
        if math.isclose(interval.a, self.a) and math.isclose(interval.b, self.b):
            return True
    
    def find_relation(self, interval):
        if self.b < interval.a:
            return _NON_OVERLAPPING_RIGHT
        if self.a > interval.b:
            return _NON_OVERLAPPING_LEFT
        if self.equals(interval):
            return _EQUALS
        if interval.a <= self.a and interval.b >= self.b:
            return _CONTAINS
        if interval.a >= self.a and interval.b <= self.b:
            return _CONTAINED_WITHIN
        if interval.a <= self.a:
            return _OVERLAPPING_LEFT
        return _OVERLAPPING_RIGHT

    def is_overlapping(self, interval):
        rel = self.find_relation(interval)
        return self.is_overlapping_rel(rel)
    
    def is_overlapping_rel(self, rel):
        return rel != _NON_OVERLAPPING_LEFT and rel != _NON_OVERLAPPING_RIGHT

    def intersect(self, interval):
        rel = self.find_relation(interval)
        if not self.is_overlapping_rel(rel):
            return IntervalSet()

        if self.a >= interval.a:
            left = self.a
            left_ind = self.ia
        else:
            left = interval.a
            left_ind = interval.ia

        if self.b <= interval.b:
            right = self.b
            right_ind = self.ib
        else:
            right = interval.b
            right_ind = interval.ib
        return IntervalSet([Interval(left, right, left_ind, right_ind)])

    def union(self, interval):
        rel = self.find_relation(interval)
        if self.is_overlapping_rel(rel):
            left = min(self.a, interval.a)
            right = max(self.b, interval.b)
            return IntervalSet(Interval(left, right))
        if rel == _NON_OVERLAPPING_RIGHT: 
            return IntervalSet([self.copy(), interval.copy()])
        return IntervalSet([interval.copy(), self.copy()])

    def subtract(self, interval):
        rel = self.find_relation(interval)
        if not self.is_overlapping_rel(rel):
            return IntervalSet(self)
        if rel == _CONTAINS:
            return IntervalSet()
        ret = IntervalSet()
        if interval.a > self.a:
            ret.add(Interval(self.a, interval.a, self.ia, interval.ia))
        if interval.b < self.b:
            ret.add(Interval(interval.b, self.b, interval.ib, self.ib))
        return ret
        

class IntervalSet:
    def __init__(self, intervals = None):
        if intervals is None:
            self.ivs = []
        elif isinstance(intervals, Interval):
            self.ivs = [intervals]
        else:
            self.ivs = intervals

    def __str__(self):
        return "[" + ", ".join([str(iv) for iv in self.ivs]) + "]"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        if len(self.ivs) != len(other.ivs):
            return False
        s = set()
        for iv in self.ivs:
            s.add(str(iv))
        for iv in other.ivs:
            if str(iv) not in s:
                return False
        return True
    
    def sort(self):
        self.ivs = sorted(self.ivs, key=lambda x: x.a)

    def inverse(self):
        if len(self.ivs) == 0:
            return IntervalSet(Interval(float('-inf'), float('inf')))
        self.sort()
    
        ret = IntervalSet()
        left = float('-inf')
        ind = 0
        left_ind = None
        while ind < len(self.ivs):
            curr_a = self.ivs[ind].a
            curr_b = self.ivs[ind].b
            if curr_a <= left:
                if curr_b <= left:
                    continue
                left = curr_b
            else:
                right = curr_a
                right_ind = self.ivs[ind].ia
                ret.add(Interval(left, right, left_ind, right_ind))

                left = curr_b
                left_ind = self.ivs[ind].ib
            ind += 1

        # Handle the last interval
        ret.add(Interval(left, float('inf'), left_ind, None))
        return ret



    def add(self, intervals):
        if isinstance(intervals, Interval):
            self.ivs.append(intervals)
        if isinstance(intervals, IntervalSet):
            for iv in intervals.ivs:
                if not iv.is_empty:
                    self.ivs.append(iv)
    
    def intersect(self, intervals):
        ret = IntervalSet()
        for iva in self.ivs:
            for ivb in intervals.ivs:
                ret.add(iva.intersect(ivb))
        return ret

    def union(self, intervals):
        ret = IntervalSet()
        for iv in self.ivs:
            ret.ivs.append(iv)
        for iv in intervals.ivs:
            ret.ivs.append(iv)
        return ret

    def subtract(self, intervals):
        return self.intersect(intervals.inverse())
    
