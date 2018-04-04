class Load:

    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return '{0}: {1}'.format(self.__class__.__name__, self.number)

    def LFormat(self):
        return ''


class NL(Load):

    def __init__(self, number, node, x_force, y_force, z_force, x_moment,
                 y_moment, z_moment, conc_mass):
        Load.__init__(self, number)
        self.node = node
        self.Fx = x_force
        self.Fy = y_force
        self.Fz = z_force
        self.Mx = x_moment
        self.My = y_moment
        self.Mz = z_moment
        self.NMass = conc_mass

    def LFormat(self):
        return ('NF,' + str(self.node) + ',' + str(self.Fx) + ','
                + str(self.Fy) + ',' + str(self.Fz) + ',' + str(self.Mx) + ','
                + str(self.My) + ',' + str(self.Mz) + ',' + str(self.NMass)
                + '\n')


class ND(Load):

    def __init__(self, number, node, x_disp, y_disp, z_disp, x_rot, y_rot,
                 z_rot):
        Load.__init__(self, number)
        self.node = node
        self.Tx = x_disp
        self.Ty = y_disp
        self.Tz = z_disp
        self.Rx = x_rot
        self.Ry = y_rot
        self.Rz = z_rot

    def LFormat(self):
        return ('ND,' + str(self.node) + ',' + str(self.Tx) + ','
                + str(self.Ty) + ',' + str(self.Tz) + ',' + str(self.Rx) + ','
                + str(self.Ry) + ',' + str(self.Rz) + '\n')


class EP(Load):

    def __init__(self, number, element, coord, length, x_force, y_force,
                 z_force, x_moment, y_moment, z_moment):
        Load.__init__(self, number)
        self.element = element
        self.coord = coord
        self.length = length
        self.Fx = x_force
        self.Fy = y_force
        self.Fz = z_force
        self.Mx = x_moment
        self.My = y_moment
        self.Mz = z_moment

    def LFormat(self):
        return ('EP,' + str(self.element) + ',' + str(self.coord) + ','
                + str(self.length) + ',' + str(self.Fx) + ',' + str(self.Fy)
                + ',' + str(self.Fz) + ',' + str(self.Mx) + ',' + str(self.My)
                + ',' + str(self.Mz) + '\n')


class LList(list):

    def __init__(self, data=[]):
        list.__init__(self, data)

    def __add__(self, other):
        return list.__add__(self, other)

    def __mul__(self, other):
        return list.__mul__(self, other)

    def __getitem__(self, key):
        return list.__getitem__(self, key)

    def __setitem__(self, key, value):
        return list.__setitem__(self, key, value)

    def __delitem__(self, key):
        return list.__delitem__(self, key)

    def add_item(self, new_item):
        index = next((i for i, item in enumerate(self)
                      if item.number == new_item.number), None)
        if index is not None:
            self[index] = new_item
        else:
            self.append(new_item)
