"""
An implementation of the Ramer–Douglas–Peucker end-point fit algorithm
using python and matplotlib. This is implemented according to the
algorithm described on the wikipedia page for Ramer-Douglas-Peucker algorithm
(https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm)
and was inspired by the Coding Train's Coding Challenge (https://www.youtube.com/watch?v=nSYw9GrakjY)
by Dan Shiffman

Pass values for epsilon in as arguments to the program.
"""

import matplotlib.pyplot
import math
import sys
from point import Point

i = 0.005


def line_sep_generator():
    o = ['--', ':', '-.']
    i = 0
    while True:
        yield o[i]
        i = (i + 1) % len(o)


ls = line_sep_generator()


def get_points(limit):
    '''
    Returns some points according to the formula
    e^-x * cos(2 * pi * x) for values of x
    from 0 up to limit.

    i is a global constant that controls the increment
    of this function as it calculates values from 0 to limit
    '''
    global i
    c = 0
    x = []
    while c < limit:
        x.append(c)
        c += i

    y = list(map(lambda v: math.exp(-v) * math.cos(2 * math.pi * v), x))
    return x, y


def rdp(points, e=0.001):
    """
    points is an ordered list of Point objects and
    e is the minimum distance to be resolved by the
    algorithm

    returns the list of ordered points which are no
    closer to the original curve than e
    """
    if len(points) <= 1:
        return points
    first = points.pop(0)
    last = points.pop()
    first.keep = True
    last.keep = True

    fIdx = -1
    fP = None
    fDist = 0
    for (i, p) in enumerate(points):
        dist = p.distance_to_line(first, last)
        if dist > fDist:
            fDist = dist
            fIdx = i
            fP = p
    if fDist > e:
        fP.keep = True
        result = []
        result.append(first)
        result.extend(rdp(points[:fIdx + 1], e))
        result.extend(rdp(points[fIdx:], e))
        result.append(last)
        return [p for p in result if p.keep]
    else:
        return [first] + [p for p in points if p.keep] + [last]


def main():
    try:
        e = [float(a) for a in sys.argv[1:]]
    except (IndexError, ValueError, TypeError):
        print('Provide one or more epsilon values for the RDP algorithm as CLI args')
        print('Try: python main.py 0.01 0.05 0.15')
        exit(1)

    # change font size
    matplotlib.rcParams.update({'font.size': 16})

    # create figure
    figure = matplotlib.pyplot.figure(figsize=(12, 8), dpi=120)

    # space for unsimplified curve
    splot = matplotlib.pyplot.subplot()
    x, y = get_points(5)
    splot.plot(x, y, linewidth=4, label='i={}, no simplification'.format(i))

    # plot each epsilon value in its own plot
    for e in sys.argv[1:]:
        epsilon = float(e)
        points = [Point(pair[0], pair[1]) for pair in zip(x, y)]
        simplified = rdp(points, epsilon)

        x = [i.x for i in simplified]
        y = [i.y for i in simplified]

        splot.plot(x, y, linestyle=next(ls), linewidth=2.5,
                   label='i={}, ε={}'.format(i, e))

    # show legend and add to figure
    splot.legend()
    splot.set_title(' '.join(sys.argv))
    figure.add_subplot(splot)

    # show the figure
    matplotlib.pyplot.show()


if __name__ == '__main__':
    main()
