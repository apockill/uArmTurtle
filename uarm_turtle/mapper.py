
class Map:
    """ This takes a list of the format
        [[x, y, dir], [x, y, dir], [x, y, dir]]
        and is able to do various operations with the information"""

    def __init__(self, turtle_log):
        self.log = turtle_log
        self.pts = [pos[0] for pos in self.log]
        self.dirs = [pos[1] for pos in self.log]

    def generate_path(self, bounds):
        """
        Returns a list of coordinates where they have been scaled to fit in the given bounds
        as well as possible.

        :param bounds: [xmin, ymin, xmax, ymax]
        :return:
        """
        pass

    def unit_vector(self):
        """ converts the log to its unit vector form """

        nums = []
        for pt in self.pts:
            nums += map(abs, pt)

        largest = max(nums)

        pts = [(pt[0] / largest, pt[1] / largest) for pt in self.pts]

        print(pts)