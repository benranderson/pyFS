class Node:

    def __init__(self, number, x_coord, y_coord, z_coord, CSYS=0):
        self.number = number
        self.x = x_coord
        self.y = y_coord
        self.z = z_coord
        self.CSYS = CSYS

    def __repr__(self):
        return 'Node {0} <{1}, {2}, {3}> CSYS={4}'.format(self.number, self.x,
                                                          self.y, self.z,
                                                          self.CSYS)
