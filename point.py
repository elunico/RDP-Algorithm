import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.keep = False

    def distance_to_line(self, l1, l2):
        x0, y0 = self.x, self.y
        x1, y1 = l1.x, l1.y
        x2, y2 = l2.x, l2.y

        n1 = (y2 - y1) * x0
        n2 = (x2 - x1) * y0
        n3 = (x2 * y1)
        n4 = (y2 * x1)
        numerator = abs(n1 - n2 + n3 - n4)

        d1 = (y2 - y1) ** 2
        d2 = (x2 - x1) ** 2
        denominator = math.sqrt(d1 + d2)

        return numerator / denominator

    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

    def __repr__(self):
        return 'Point{}'.format(self.__str__())
