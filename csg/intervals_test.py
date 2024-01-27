import unittest
import intervals as iv
from parameterized import parameterized


class TestInterval(unittest.TestCase):

    @parameterized.expand([
        (iv.Interval(2, 3), iv.Interval(4, 5), iv._NON_OVERLAPPING_RIGHT),
        (iv.Interval(2, 3), iv.Interval(0, 1), iv._NON_OVERLAPPING_LEFT),
        (iv.Interval(2, 3), iv.Interval(-5, -3), iv._NON_OVERLAPPING_LEFT),
        (iv.Interval(2, 3), iv.Interval(1, 2.5), iv._OVERLAPPING_LEFT),
        (iv.Interval(2, 3), iv.Interval(2.5, 4), iv._OVERLAPPING_RIGHT),
        (iv.Interval(2.1, 3.2), iv.Interval(2.1, 3.2), iv._EQUALS),
        (iv.Interval(2, 3), iv.Interval(1, 4), iv._CONTAINS),
        (iv.Interval(2.1, 3.2), iv.Interval(2.1, 4), iv._CONTAINS),
        (iv.Interval(2.1, 3.2), iv.Interval(1.1, 3.2), iv._CONTAINS),
        (iv.Interval(2.1, 2.9), iv.Interval(2.2, 2.8), iv._CONTAINED_WITHIN),
        (iv.Interval(2.1, 2.9), iv.Interval(2.2, 2.9), iv._CONTAINED_WITHIN),
        (iv.Interval(2.1, 3), iv.Interval(2.1, 2.9), iv._CONTAINED_WITHIN),
    ])
    def test_find_relation(self, interval1, interval2, expected):
        self.assertEqual(expected, interval1.find_relation(interval2))
     

    @parameterized.expand([
        (iv.Interval(2, 4, 1), iv.Interval(3.1, 5, 2), iv.IntervalSet(iv.Interval(3.1, 4, 2, 1))),
        (iv.Interval(2, 4, 1), iv.Interval(3.1, 3.7, 2), iv.IntervalSet(iv.Interval(3.1, 3.7, 2))),
        (iv.Interval(2, 4, 1), iv.Interval(4, 5, 2), iv.IntervalSet(iv.Interval(4, 4, 2, 1))),
        (iv.Interval(2, 4, 1), iv.Interval(5, 6, 2), iv.IntervalSet()),
        (iv.Interval(2, 4, 1), iv.Interval(3, float('inf'), 2, None), iv.IntervalSet(iv.Interval(3, 4, 2, 1))),
        (iv.Interval(2, 4, 1), iv.Interval(float('-inf'), float('inf')), iv.IntervalSet(iv.Interval(2, 4, 1, 1))),
    ])
    def test_intersect(self, interval1, interval2, expected):
        self.assertEqual(expected, interval1.intersect(interval2))

    # @parameterized.expand([
    #     (iv.Interval(2, 4, 1), iv.Interval(5, 6), 2, iv.IntervalSet([iv.Interval(2, 4, 1), iv.Interval(5, 6, 2)])),
    #     (iv.Interval(5, 6), iv.Interval(2, 4), iv.IntervalSet([iv.Interval(2, 4), iv.Interval(5, 6)])),
    #     (iv.Interval(2, 4), iv.Interval(3, 5), iv.IntervalSet(iv.Interval(2, 5))),
    #     (iv.Interval(2, 4), iv.Interval(1, 6), iv.IntervalSet(iv.Interval(1, 6))),
    #     (iv.Interval(1, 6), iv.Interval(2, 4), iv.IntervalSet(iv.Interval(1, 6))),
    #     (iv.Interval(2, 4), iv.Interval(1, 3), iv.IntervalSet(iv.Interval(1, 4))),
    #     (iv.Interval(2, 4), iv.Interval(4, 5), iv.IntervalSet(iv.Interval(2, 5))),
    #     (iv.Interval(2, 4, 1), iv.Interval(4, float('inf'), 2, None), iv.IntervalSet(iv.Interval(2, float('inf'), 1, None))),
    # ])
    # def test_union(self, interval1, interval2, expected):
    #     self.assertEqual(expected, interval1.union(interval2))


class TestIntervals(unittest.TestCase):

    @parameterized.expand([
        (
            iv.IntervalSet([iv.Interval(2, 4, 1), iv.Interval(15, 16, 3)]),
            iv.IntervalSet([iv.Interval(1, 3, 2), iv.Interval(8, 18, 4)]),
            iv.IntervalSet([iv.Interval(1, 3, 2), iv.Interval(2, 4, 1), iv.Interval(8, 18, 4), iv.Interval(15, 16, 3)]),
        )
    ])
    def test_union(self, intervals1, intervals2, expected):
        self.assertEqual(expected, intervals1.union(intervals2))

    @parameterized.expand([
        (
            iv.IntervalSet([iv.Interval(2, 4, 1), iv.Interval(8, 10, 3)]),
            iv.IntervalSet([iv.Interval(3, 9, 2), iv.Interval(9.5, 9.6, 4)]),
            iv.IntervalSet([iv.Interval(3, 4, 2, 1), iv.Interval(8, 9, 3, 2), iv.Interval(9.5, 9.6, 4)]),
        )
    ])
    def test_intersect(self, intervals1, intervals2, expected):
        self.assertEqual(expected, intervals1.intersect(intervals2))

    @parameterized.expand([
        (
            iv.IntervalSet([iv.Interval(2, 4, 1), iv.Interval(8, 10, 3)]),
            iv.IntervalSet([iv.Interval(float('-inf'), 2, None, 1), iv.Interval(4, 8, 1, 3), iv.Interval(10, float('inf'), 3, None)]),
        )
    ])
    def test_inverse(self, intervals, expected):
        self.assertEqual(expected, intervals.inverse())

    @parameterized.expand([
        (
            iv.IntervalSet([iv.Interval(2, 6, 3)]),
            iv.IntervalSet([iv.Interval(4, 7, 5)]),
            iv.IntervalSet([iv.Interval(2, 4, 3, 5)]),
        ),
        (
            iv.IntervalSet([iv.Interval(2, 6, 3)]),
            iv.IntervalSet([iv.Interval(3, 4, 2), iv.Interval(8, 9, 4)]),
            iv.IntervalSet([iv.Interval(2, 3, 3, 2), iv.Interval(4, 6, 2, 3)]),
        ),
        (
            iv.IntervalSet([iv.Interval(2, 3, 3)]),
            iv.IntervalSet([iv.Interval(4, 6, 2), iv.Interval(5, 7, 4)]),
            iv.IntervalSet([iv.Interval(2, 3, 3, 3)]),
        ),
        (
            iv.IntervalSet([iv.Interval(2, 4, 1), iv.Interval(8, 10, 3)]),
            iv.IntervalSet([iv.Interval(3, 9, 2), iv.Interval(9.5, 9.6, 4)]),
            iv.IntervalSet([iv.Interval(2, 3, 1, 2), iv.Interval(9, 9.5, 2, 4), iv.Interval(9.6, 10, 4, 3)]),
        )
    ])
    def test_subtract(self, intervals1, intervals2, expected):
        print(intervals1.subtract(intervals2))
        self.assertEqual(expected, intervals1.subtract(intervals2))

        


if __name__ == '__main__':
    unittest.main()