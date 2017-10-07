from copy import deepcopy
from itertools import groupby

import numpy as np

class Map:
    """ This takes a list of the format
        [[x, y], [x, y], [x, y]]
        and is able to do various operations with the information"""

    def __init__(self, map=None):
        if map is not None:
            self.pts = deepcopy(map.pts)
            self.pen_down = deepcopy(map.pen_down)
        else:
            self.pts = []
            self.pen_down = []  # A list of pen_down state for every pt

    def __repr__(self):
        return str(self.pts)

    def __len__(self):
        return len(self.pts)

    def append(self, coord, pen_down):
        self.pts.append(coord)
        self.pen_down.append(pen_down)

    def fit_to(self, bounds):
        """
        Returns a list of coordinates where they have been scaled to fit in the given bounds
        as well as possible.

        :param bounds: [xmin, ymin, xmax, ymax]
        :return:
        """
        copy = self.copy()
        unit = copy.unit_vector()
        scale_by = min([bounds[2] - bounds[0], bounds[3] - bounds[1]])


        scaled = unit.scale(scale_by)
        lowest_x = min([pt[0] for pt in scaled.pts])
        lowest_y = min([pt[1] for pt in scaled.pts])

        translate_x = bounds[0] - lowest_x
        translate_y = bounds[1] - lowest_y

        translated = scaled.translate(translate_x, translate_y)
        return translated.to_int()

    def translate(self, translate_x, translate_y):
        copy = self.copy()
        copy.pts = [[ptx + translate_x, pty + translate_y] for ptx, pty in copy.pts]
        return copy

    def unit_vector(self):
        """ converts the log to its unit vector form """
        copy = self.copy()

        nums = []
        for pt in copy.pts:
            nums += map(abs, pt)

        largest = max(nums)

        copy.pts = [(pt[0] / largest, pt[1] / largest) for pt in copy.pts]
        return copy

    def to_int(self):
        """ Round and convert to integers """
        copy = self.copy()
        copy.pts = [[int(round(ptx, 0)), int(round(pty, 0))] for ptx, pty in copy.pts]
        return copy

    def get_lines(self):
        """ Returns a list of lines with the format
        [[[x1, y1], [x2, y2]], [[x2, y2], [x3, y3]], [[x3, y3, [x4, y4]]]
        """
        copy = self.copy()
        lines = []
        last_pt = [copy.pts[0][0], copy.pts[0][1]]
        for ptx, pty in copy.pts[1:]:
            lines.append([last_pt, [ptx, pty]])
            last_pt = [ptx, pty]

        return lines

    def scale(self, weight):
        # Scale internal points
        copy = self.copy()
        copy.pts = [[ptx * weight, pty * weight] for ptx, pty in copy.pts]
        return copy

    def copy(self):
        return deepcopy(self)